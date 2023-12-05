FROM python:3.9-slim-buster

WORKDIR /microservice1

RUN pip install flask prometheus_client psutil

COPY . /microservice1

EXPOSE 5000

ENV FLASK_APP=hello.py

CMD ["flask", "run", "--host", "0.0.0.0"]