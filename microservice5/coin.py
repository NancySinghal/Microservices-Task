from flask import Flask, render_template
from prometheus_client import Counter, Gauge, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST
import random

app = Flask(__name__)

# Custom metrics
flips_counter = Counter('coin_flips_total', 'Total number of coin flips')
heads_counter = Counter('heads_total', 'Total number of heads')
tails_counter = Counter('tails_total', 'Total number of tails')
ratio_heads_to_tails = Gauge('ratio_heads_to_tails', 'Ratio of heads to tails')

@app.route('/')
def flip_coin():
    result = flip()
    
    # Increment custom metrics
    flips_counter.inc()
    if result == 'heads':
        heads_counter.inc()
    else:
        tails_counter.inc()

    # Update ratio metric
    total_heads = heads_counter._value.get()
    total_tails = tails_counter._value.get()
    ratio_heads_to_tails.set(total_heads / max(total_tails, 1))

    return render_template('coin_flip.html', result=result)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

def flip():
    return random.choice(['heads', 'tails'])

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
