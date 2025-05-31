from flask import Flask, request
import time
import logging
import random
from prometheus_client import start_http_server, Counter, Histogram

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Prometheus Metrics
REQUEST_COUNTER = Counter(
    'http_requests_total', 'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'Request Latency',
    ['method', 'endpoint']
)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.method, request.path).observe(resp_time)
    REQUEST_COUNTER.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route("/")
def index():
    app.logger.info("Visited home endpoint")
    return "Hello from demo app first!", 200

@app.route("/error")
def error():
    app.logger.error("Simulated error occurred")
    return "Error simulated first", random.choice([400, 404, 500])

if __name__ == "__main__":
    start_http_server(8003)  # Prometheus metrics port
    app.run(host="0.0.0.0", port=5003)
