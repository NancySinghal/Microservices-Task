from flask import Flask, render_template, request
from prometheus_client import Counter, Gauge, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST

app = Flask(__name__)

# Custom metrics
greetings_counter = Counter('greetings_total', 'Total number of greetings')
unique_names_greeted = Gauge('unique_names_greeted', 'Number of unique names greeted')

# Set for unique names
unique_names = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['name']
    greeting = f'Hello, {name}!'

    # Increment metric
    greetings_counter.inc()

    # Add to the set 
    unique_names.add(name)

    # Update metric
    unique_names_greeted.set(len(unique_names))

    return render_template('greet.html', greeting=greeting)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
