from __future__ import annotations

import os
import time
from typing import Any

from fastapi import FastAPI, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

APP_NAME = os.getenv("APP_NAME", "cloud-native-api")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

app = FastAPI(
    title="Cloud-Native Infrastructure API",
    version=APP_VERSION,
    description=(
        "A portfolio-grade backend service demonstrating API engineering, "
        "containerisation, observability and CI/CD readiness."
    ),
)


@app.middleware("http")
async def metrics_middleware(request: Any, call_next: Any) -> Response:
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    path = request.url.path
    REQUEST_COUNT.labels(request.method, path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, path).observe(elapsed)
    return response


@app.get("/health", tags=["Operations"])
def health() -> dict[str, str]:
    return {"status": "healthy", "service": APP_NAME}


@app.get("/api/v1/info", tags=["Platform"])
def service_info() -> dict[str, str]:
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "environment": os.getenv("APP_ENV", "development"),
        "runtime": "Python + FastAPI",
        "role": "backend-infrastructure-reference-service",
    }


@app.get("/api/v1/items/{item_id}", tags=["API"])
def get_item(item_id: int) -> dict[str, Any]:
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="item_id must be positive")
    return {
        "id": item_id,
        "name": f"infrastructure-item-{item_id}",
        "status": "active",
    }


@app.get("/metrics", tags=["Operations"])
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
