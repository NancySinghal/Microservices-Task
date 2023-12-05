from flask import Flask, render_template, request
from prometheus_client import Counter, Gauge, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST

app = Flask(__name__)

# Custom metrics
tasks_counter = Counter('tasks_total', 'Total number of tasks')
remaining_tasks = Gauge('remaining_tasks', 'Number of remaining tasks to complete')

tasks = []

@app.route('/')
def todo_list():
    return render_template('todo.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    tasks.append(task)

    # Increment metric
    tasks_counter.inc()

    # Update metric
    remaining_tasks.set(len(tasks))

    return render_template('todo.html', tasks=tasks)

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    if task_id < len(tasks):
        tasks.pop(task_id)

        # Update metric
        remaining_tasks.set(len(tasks))

    return render_template('todo.html', tasks=tasks)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
