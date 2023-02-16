# syntax = docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /logmine

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "-m", "flask", "run"]

# CMD ["python3", "app.py"]
