from flask import Flask, request
import time
import logging
import random
from prometheus_client import start_http_server, Counter, Histogram
from fluent import handler as fluent_handler
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

# 🔧 Fluent Bit TCP Logging
fluent = fluent_handler.FluentHandler('app.logs', host='fluent-bit', port=24224)
fluent_formatter = fluent_handler.FluentRecordFormatter({
    'host': '%(hostname)s',
    'where': '%(module)s.%(funcName)s',
    'message': '%(message)s',
    'level': '%(levelname)s',
    'remote_addr': '%(remote_addr)s',
    'endpoint': '%(endpoint)s',
    'status_code': '%(status_code)s'
})
fluent.setFormatter(fluent_formatter)
app.logger.addHandler(fluent)

app.logger.setLevel(logging.INFO)

# 📈 Prometheus Metrics
REQUEST_COUNTER = Counter(
    'http_requests_total', 'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'Request Latency',
    ['method', 'endpoint']
)

# ⏱️ Track start time before request
@app.before_request
def start_timer():
    request.start_time = time.time()

# 📊 Record metrics and log after response
@app.after_request
def record_metrics(response):
    resp_time = time.time() - request.start_time

    method = request.method
    endpoint = request.path
    status = str(response.status_code)

    # Prometheus
    REQUEST_LATENCY.labels(method, endpoint).observe(resp_time)
    REQUEST_COUNTER.labels(method, endpoint, status).inc()

    # Structured log to Fluent Bit
    app.logger.info(
        f"{method} {endpoint} returned {status}",
        extra={
            "remote_addr": request.remote_addr,
            "endpoint": endpoint,
            "status_code": status
        }
    )
    return response

# 🟢 Normal Endpoint with Log
@app.route("/")
def index():
    app.logger.info(
        "Visited home endpoint",
        extra={
            "remote_addr": request.remote_addr,
            "endpoint": request.path,
            "status_code": 200
        }
    )
    return "Hello from demo app first!", 200

# 🔴 Simulate Error with Log
@app.route("/error")
def error():
    code = random.choice([400, 404, 500])
    app.logger.error("Simulated error occurred", extra={
        "remote_addr": request.remote_addr,
        "endpoint": request.path,
        "status_code": code
    })
    return "Error simulated", code

# 🚀 Start Server
if __name__ == "__main__":
    start_http_server(8003)
    app.run(host="0.0.0.0", port=5003)
