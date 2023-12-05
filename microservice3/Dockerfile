FROM python:3.9-slim-buster

WORKDIR /microservice3

RUN pip install flask prometheus_client psutil

COPY . /microservice3

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host", "0.0.0.0"]