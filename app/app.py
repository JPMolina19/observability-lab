from flask import Flask, Response
from prometheus_client import Counter, generate_latest, Histogram
import time


app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total application requests",
    ["endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Application request latency"
)

@app.route("/")
def home():

    start_time = time.time()

    REQUEST_COUNT.labels(
        endpoint="/",
        status="200"
    ).inc()

    time.sleep(0.2)

    REQUEST_LATENCY.observe(
        time.time() - start_time
    )

    return "Observability Lab Running"


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype="text/plain"
    )


@app.route("/error")
def error():
    REQUEST_COUNT.labels(endpoint="/error", status="500").inc()
    return "Simulated application error", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)