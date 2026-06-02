# Production Readiness

This repo is a deployable portfolio reference. For production, extend it with:

## Storage

- Persistent storage for Grafana, Prometheus, Loki, and Tempo
- Object storage backend for Loki and Tempo
- Retention policies

## Security

- Replace demo credentials
- Configure SSO/OIDC for Grafana and Headlamp
- Use TLS on all ingress
- Apply NetworkPolicy
- Use external secrets

## Scale

- Loki scalable mode
- Tempo distributed mode
- Prometheus remote write or Thanos/Mimir
- Dedicated ingestion and query layers

## Reliability

- PodDisruptionBudgets
- Requests and limits
- Backup dashboards and configs
- Monitor the observability platform itself

## Governance

- Standard labels
- Telemetry ownership
- Retention standards
- Dashboards-as-code
