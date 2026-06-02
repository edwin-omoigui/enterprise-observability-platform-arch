#!/usr/bin/env bash
set -euo pipefail
echo "Grafana:    http://127.0.0.1:3000"
echo "Headlamp:   http://127.0.0.1:4466"
echo "Sample App: http://127.0.0.1:8080"
kubectl -n observability port-forward svc/grafana 3000:80 &
kubectl -n observability port-forward svc/headlamp 4466:80 &
kubectl -n demo port-forward svc/sample-otel-app 8080:80 &
wait
