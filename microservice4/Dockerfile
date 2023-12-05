FROM python:3.9-slim-buster

WORKDIR /microservice4

RUN pip install flask prometheus_client psutil structlog

COPY . /microservice4

EXPOSE 5000

ENV FLASK_APP=calculator.py

CMD ["flask", "run", "--host", "0.0.0.0"]