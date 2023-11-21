# connector-for-jira

## Introdução
Este script em Python tem como objetivo integrar informações entre o SonarQube e o Jira para realizar a gestão de questões de segurança em projetos de software. O código utiliza a biblioteca `jira` para interação com o Jira e `sonarqube` para interação com o SonarQube, permitindo a criação automática de tarefas no Jira com base nas vulnerabilidades identificadas no SonarQube.

## Configuração
Antes de executar o script, é necessário configurar algumas variáveis de ambiente:

- `SONAR_URL`: URL do servidor SonarQube.
- `USERNAME_SONAR`: Nome de usuário para autenticação no SonarQube.
- `TOKEN_SONAR`: Token de acesso para autenticação no SonarQube.
- `USERNAME_JIRA`: Nome de usuário para autenticação no Jira.
- `PASSWORD_JIRA`: Senha para autenticação no Jira.
- `JIRA_URL`: URL do servidor Jira.

Além disso, o script espera um arquivo JSON chamado `projectslist.json`, que contém informações sobre os projetos a serem monitorados.

## Funcionalidades Principais

### 1. Conexão com o SonarQube e Jira
O script inicia criando instâncias dos clientes do SonarQube e do Jira, utilizando as informações de autenticação fornecidas nas variáveis de ambiente.

```python
sonar_client = SonarQubeClient(sonarqube_url=getenv('SONAR_URL'), username=getenv('USERNAME_SONAR'), token=getenv('TOKEN_SONAR'))
jira_client = JIRA(basic_auth=(getenv('USERNAME_JIRA'), getenv('PASSWORD_JIRA')), options={'server': getenv('JIRA_URL')})
```

### 2. Resgate de Dados dos Projetos
Os dados dos projetos são recuperados a partir de um arquivo JSON chamado projectslist.json. Esses dados incluem o nome do projeto, o projeto no SonarQube e o projeto no Jira.

```python
def projects_list():
    # ...
```

### 3. Comparação entre Dados do SonarQube e Jira
O script então compara as questões de segurança identificadas no SonarQube com as existentes no Jira. Ele utiliza as APIs do SonarQube e Jira para buscar informações sobre vulnerabilidades e hotspots de segurança.

```python
def get_all_sonarqube_and_jira_issues(projects_list):
    # ...
```

### 4. Criação de Tarefas no Jira
Com base nas comparações, o script cria novas tarefas no Jira para questões de segurança identificadas no SonarQube que ainda não foram registradas no Jira.

```python
def creat_issue_jira(issues_in_sonar, hotspots_in_sonar, issues_in_jira, sonar_project, jira_project, project_name):
    # ...
```

### Execução
O script principal é executado quando o arquivo é chamado como um programa principal (__name__ == "__main__"). Ele inicia o processo chamando a função projects_list().

```python
if __name__ == "__main__":
    projects_list()
```

### Considerações Finais
Este script fornece uma maneira automatizada de gerenciar tarefas de segurança no Jira com base nas informações obtidas do SonarQube. É crucial garantir que as configurações no Jira estejam corretas e que o arquivo JSON de configuração esteja atualizado para refletir os projetos relevantes. Em caso de erro, mensagens detalhadas de erro são registradas nos logs.
