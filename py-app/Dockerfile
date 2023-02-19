FROM tiangolo/uwsgi-nginx-flask:python3.7

WORKDIR /py-app

RUN pip3 install https://github.com/trungdq88/logmine.git

RUN chmod +x logmine

COPY . .

EXPOSE 8080

# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]

CMD ["python3", "main.py"]
