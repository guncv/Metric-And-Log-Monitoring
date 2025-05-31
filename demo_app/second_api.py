# demo_app/app.py
from flask import Flask
import logging
import random
from prometheus_client import start_http_server, Counter

app = Flask(__name__)

# Logs
logging.basicConfig(level=logging.INFO)

# Prometheus Metrics
REQUEST_COUNTER = Counter('demo_requests_total', 'Total Requests')

@app.route("/")
def index():
    REQUEST_COUNTER.inc()
    app.logger.info("Visited home endpoint")
    return "Hello from demo app!"

@app.route("/error")
def error():
    REQUEST_COUNTER.inc()
    app.logger.error("Simulated error occurred")
    return "Error simulated", 500

if __name__ == "__main__":
    start_http_server(8002)
    app.run(host='0.0.0.0', port=5002)
