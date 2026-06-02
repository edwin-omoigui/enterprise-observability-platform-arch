# Observability Platform Architecture

## Purpose

This architecture demonstrates a Kubernetes observability platform using the Grafana ecosystem and OpenTelemetry.

## Layers

| Layer | Component | Responsibility |
|---|---|---|
| Application | Sample app | Emits metrics, logs, and traces |
| Collection | Grafana Alloy | Receives, discovers, enriches, routes telemetry |
| Metrics | Prometheus | Stores and queries metrics |
| Logs | Loki | Stores and queries logs |
| Traces | Tempo | Stores and queries distributed traces |
| Visualization | Grafana | Dashboards, Explore, cross-signal analysis |
| Kubernetes UI | Headlamp | Cluster and workload visibility |

## Design Principles

- OpenTelemetry-first instrumentation
- Collector-based telemetry routing
- Metrics, logs, and traces together
- Kubernetes-native deployment
- Dashboards-as-code
- Platform and application troubleshooting alignment
