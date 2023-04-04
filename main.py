import logging
import json
from os import getenv
from jira import  JIRA
from sonarqube import SonarQubeClient

#Conexão OAuth SonarQube e Jira
sonar_client = SonarQubeClient(sonarqube_url=getenv('SONAR_URL'), username=getenv('USERNAME_SONAR'), token=getenv('TOKEN_SONAR'))
jira_client = JIRA(basic_auth=(getenv('USERNAME_JIRA'), getenv('PASSWORD_JIRA')), options = {'server': getenv('JIRA_URL')})

customfield = 'customfield_10222'

#Resgatando os dados dos projetos do arquivo JSON
def projects_list():
    with open("projectslist.json", "r") as jsonfile:
        projects_list = json.load(jsonfile)
        get_all_sonarqube_and_jira_issues(projects_list)

#Resgatando os dados tanto do Sonarqube quanto do Jira para posteriormente fazer as devidas comparações de igualdade
def get_all_sonarqube_and_jira_issues(projects_list):
    for i in projects_list:
        try:
            #chamando a API do SonarQube e armazenando o json retornando
            project_name = f"{i['ProjectName']}"
            sonar_project = f"{i['SonarProject']}"
            jira_project = f"{i['JiraProject']}"

            issues_in_sonar = list(sonar_client.issues.search_issues(componentKeys=sonar_project, branch="master", types="VULNERABILITY"))
            hotspots_in_sonar = list(sonar_client.hotspots.search_hotspots(projectKey=sonar_project, branch="master", vulnerabilityProbability="MEDIUM"))

            #chamando a API do Jira e armazenando o json retornando   
            search_jira = jira_client.search_issues(f"project={jira_project} AND type = Security ", json_result=True, fields=customfield)
            issues_in_jira = search_jira.get('issues')
            
            creat_issue_jira(issues_in_sonar, hotspots_in_sonar, issues_in_jira, sonar_project, jira_project, project_name)

        except Exception as error:
            logging.exception ("Erro ao recuperar os dados do projeto: " f"{i['ProjectName']} \n Verifique se a configuração no Jira está correta, ou se alguma informação no arquivo JSON está errada." f"\n{error}")
            print ("Erro ao recuperar os dados do projeto: " f"{i['ProjectName']} \n Verifique se a configuração no Jira está correta, ou se alguma informação no arquivo JSON está errada." f"\n{error}") 
            continue 

#criando novas tasks no jira
def creat_issue_jira(issues_in_sonar, hotspots_in_sonar, issues_in_jira, sonar_project, jira_project, project_name):

    #criando e populando a lista de issues do Jira relacionadas ao SonarQube
    jira_key_list = []
    for i in issues_in_jira:  
        fields = i.get('fields')
        jira_key_list.append(f"{fields[(customfield)]}")

    #se caso a key(vulnerabilidade) do SonarQube não existir no Jira irá criar uma nova task
    for i in issues_in_sonar:
        sonar_key= f"{i['key']}"
        if sonar_key in jira_key_list:
            continue
        else:
            try:
                summary = f"[{project_name}] " f"{i['message']}"
                description = "Local: " f"{i['component']}" "\n Line: " f"{i['textRange']}" f"\n URL: https://sonarqube.hucloud.com.br/project/issues?resolved=false&types=VULNERABILITY&id={sonar_project}&open={sonar_key}"
                jira_client.create_issue(project=jira_project, summary=summary[:254], customfield_10222=sonar_key, description=description, issuetype={'name': 'Security'})
                print (f"{sonar_key} Success created!")
            except Exception as error:
                logging.exception (f"Erro ao criar uma task no Jira do tipo 'Vulnerabilidade'! \n Sonar Key: " f"{sonar_key}" f"\n{error}")
                print (f"Erro ao criar uma task no Jira do tipo 'Vulnerabilidade'! \n Sonar Key: " f"{sonar_key}" f"\n{error}")
                continue        

    #se caso a key(hotspot) do SonarQube não existir no Jira irá criar uma nova task
    for i in hotspots_in_sonar:    
        sonar_key = f"{i['key']}"  
        if sonar_key in jira_key_list:
            continue
        else:
            try:
                summary = f"[{project_name}] " f"{i['message']}"
                description ="Local: " f"{i['component']}" "\n Line: " f"{i['line']}" f"\n URL: https://sonarqube.hucloud.com.br/security_hotspots?id={sonar_project}&hotspots={sonar_key}"
                jira_client.create_issue(project=jira_project, summary=summary[:254], customfield_10222=sonar_key, description=description, issuetype={'name': 'Security'})
                print (f"{sonar_key} Success created!")
            except Exception as error:
                logging.exception (f"Erro ao criar uma task no Jira do tipo 'Hotspot'! \n Sonar Key: " f"{sonar_key}" f"\n{error}")
                print (f"Erro ao criar uma task no Jira do tipo 'Hotspot'! \n Sonar Key: " f"{sonar_key}" f"\n{error}")
                continue

if __name__ == "__main__":
    projects_list()
