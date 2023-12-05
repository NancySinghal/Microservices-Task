from flask import Flask, render_template, request
from prometheus_client import Counter, Gauge, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST
import structlog

app = Flask(__name__)

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

# Create a structured logger
logger = structlog.get_logger()

# Custom metrics
calculations_counter = Counter('calculations_total', 'Total number of calculations')
error_counter = Counter('errors_total', 'Total number of errors during calculations')
average_result = Gauge('average_result', 'Average result of calculations')

total_results = 0
total_calculations = 0

@app.route('/')
def index():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    global total_results, total_calculations

    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    operation = request.form['operation']

    try:
        result = perform_calculation(num1, num2, operation)

        # Increment metric
        calculations_counter.inc()

        # Update metrics
        total_results += result
        total_calculations += 1
        average_result.set(total_results / total_calculations)

        # Log
        logger.info("Calculation succeeded", num1=num1, num2=num2, operation=operation, result=result)

    except ZeroDivisionError as e:
        # Increment counter
        error_counter.inc()

        # Log the error
        logger.error("Calculation failed - Division by zero", num1=num1, num2=num2, operation=operation, error=str(e))
        result = 'Error: Division by zero is not allowed'

    return render_template('calculator.html', result=result)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

def perform_calculation(num1, num2, operation):
    if operation == 'add':
        return num1 + num2
    elif operation == 'subtract':
        return num1 - num2
    elif operation == 'multiply':
        return num1 * num2
    elif operation == 'divide':
        return num1 / num2
    else:
        raise ValueError('Invalid operation')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
