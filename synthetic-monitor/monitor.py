import os
import time
import requests

from prometheus_client import start_http_server, Gauge


CHECK_STATUS = Gauge(
    "synthetic_check_success",
    "Synthetic check success status (1 for success, 0 for failure)"
)

RESPONSE_TIME = Gauge(
    "synthetic_response_time_seconds",
    "Synthetic response time"
)

HTTP_STATUS = Gauge(
    "synthetic_http_status_code",
    "HTTP status code returned by the synthetic check"
)


TARGET_URL = os.getenv("TARGET_URL", "http://app:5000")


def check_application():
    try:
        start = time.time()

        response = requests.get(
            TARGET_URL,
            timeout=5
        )

        elapsed = time.time() - start

        RESPONSE_TIME.set(elapsed)
        HTTP_STATUS.set(response.status_code)

        if response.status_code == 200:
            CHECK_STATUS.set(1)
            print(
                f"Synthetic check SUCCESS | "
                f"status={response.status_code} | "
                f"response_time={elapsed:.3f}s",
                flush=True
            )
        else:
            CHECK_STATUS.set(0)
            print(
                f"Synthetic check FAILED | "
                f"status={response.status_code}",
                flush=True
            )

    except Exception as error:
        CHECK_STATUS.set(0)
        RESPONSE_TIME.set(5)
        HTTP_STATUS.set(0)

        print(
            f"Synthetic check ERROR: {error}",
            flush=True
        )


if __name__ == "__main__":
    start_http_server(8000)

    print(
        f"Synthetic monitor started. Target: {TARGET_URL}",
        flush=True
    )

    while True:
        check_application()
        time.sleep(30)