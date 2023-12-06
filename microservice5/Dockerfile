FROM python:3.9-slim-buster

WORKDIR /microservice5

RUN pip install flask prometheus_client psutil

COPY . /microservice5

EXPOSE 5000

ENV FLASK_APP=coin.py

CMD ["flask", "run", "--host", "0.0.0.0"]