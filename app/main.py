import logging
import os
import random
import time

from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "sample-otel-app")
OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://alloy.observability.svc.cluster.local:4318")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s service=%(name)s trace_id=%(otelTraceID)s span_id=%(otelSpanID)s message=%(message)s",
)
logger = logging.getLogger(SERVICE_NAME)

resource = Resource.create({
    "service.name": SERVICE_NAME,
    "deployment.environment": os.getenv("ENVIRONMENT", "demo"),
})

provider = TracerProvider(resource=resource)
provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint=f"{OTLP_ENDPOINT}/v1/traces")
    )
)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

LoggingInstrumentor().instrument(set_logging_format=False)

REQUEST_COUNT = Counter(
    "sample_app_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "sample_app_request_duration_seconds",
    "Request latency in seconds",
    ["endpoint"],
)

WORK_UNITS = Counter(
    "sample_app_work_units_total",
    "Simulated work units completed",
    ["type"],
)

app = FastAPI(title="Sample OpenTelemetry App", version="1.0.0")
FastAPIInstrumentor.instrument_app(app)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(duration)
    logger.info(
        "request completed path=%s status=%s duration=%.4f",
        request.url.path,
        response.status_code,
        duration,
    )
    return response


@app.get("/")
def root():
    logger.info("root endpoint called")
    return {
        "service": SERVICE_NAME,
        "message": "Sample app emitting metrics, logs, and traces",
        "endpoints": ["/health", "/work", "/error", "/metrics"],
    }


@app.get("/health")
def health():
    logger.info("health check passed")
    return {"status": "healthy"}


@app.get("/work")
def work():
    with tracer.start_as_current_span("simulate-work") as span:
        work_type = random.choice(["cpu", "io", "database", "cache"])
        duration = random.uniform(0.05, 0.4)
        span.set_attribute("work.type", work_type)
        span.set_attribute("work.duration", duration)
        logger.info("starting simulated work type=%s duration=%.3f", work_type, duration)
        time.sleep(duration)
        WORK_UNITS.labels(type=work_type).inc()
        logger.info("completed simulated work type=%s", work_type)
        return {
            "status": "completed",
            "work_type": work_type,
            "duration_seconds": round(duration, 3),
        }


@app.get("/error")
def error(response: Response):
    with tracer.start_as_current_span("simulate-error") as span:
        span.set_attribute("error.simulated", True)
        logger.error("simulated application error")
        response.status_code = 500
        return {"status": "error", "message": "simulated error for observability testing"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
