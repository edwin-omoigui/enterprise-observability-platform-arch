#!/usr/bin/env bash
set -euo pipefail
kubectl apply -f platform/namespace.yaml

helm upgrade --install prometheus prometheus-community/prometheus --namespace observability -f platform/prometheus-values.yaml
helm upgrade --install loki grafana/loki --namespace observability -f platform/loki-values.yaml
helm upgrade --install tempo grafana/tempo --namespace observability -f platform/tempo-values.yaml
helm upgrade --install alloy grafana/alloy --namespace observability -f platform/alloy-values.yaml
helm upgrade --install grafana grafana/grafana --namespace observability -f platform/grafana-values.yaml
helm upgrade --install headlamp headlamp/headlamp --namespace observability -f platform/headlamp-values.yaml

kubectl -n observability get pods
