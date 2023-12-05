from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

request_counter = Counter('flask_requests_total', 'Total number of requests received')

@app.route('/')
def hello_world():
    request_counter.inc()
    return 'Hello, World!'

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
