FROM python:3.9.12-slim AS base
    ENV APPDIR /code
    WORKDIR $APPDIR

    COPY requirements.txt requirements.txt
    RUN pip3 install --upgrade pip
    COPY . .

    RUN pip3 install -r requirements.txt

    CMD ["./main.py"]
    ENTRYPOINT ["python3"]
