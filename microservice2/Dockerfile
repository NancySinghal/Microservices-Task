FROM python:3.9-slim-buster

WORKDIR /microservice2

RUN pip install flask prometheus_client psutil

COPY . /microservice2

EXPOSE 5000

ENV FLASK_APP=todo.py

CMD ["flask", "run", "--host", "0.0.0.0"]