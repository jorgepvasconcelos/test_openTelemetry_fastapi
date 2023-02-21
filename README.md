# test_openTelemetry_fastapi

autoinstrument commnad

    OTEL_SERVICE_NAME=fast2 OTEL_TRACES_EXPORTER=otlp OTEL_METRICS_EXPORTER=otlp OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://0.0.0.0:4317 opentelemetry-instrument uvicorn main:
    app
