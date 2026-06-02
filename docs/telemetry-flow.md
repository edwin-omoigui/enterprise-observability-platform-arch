# Telemetry Flow

## Metrics

```text
Sample App /metrics
        ↓
Grafana Alloy scrape
        ↓
Prometheus
        ↓
Grafana
```

## Logs

```text
Application stdout
        ↓
Grafana Alloy Kubernetes log discovery
        ↓
Loki
        ↓
Grafana Explore
```

## Traces

```text
OpenTelemetry SDK
        ↓
OTLP HTTP
        ↓
Grafana Alloy OTLP receiver
        ↓
Tempo
        ↓
Grafana Explore
```

## Correlation

The sample app emits:

- service name
- endpoint
- status code
- trace ID
- span ID
- structured logs
- Prometheus metrics
