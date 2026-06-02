#!/usr/bin/env bash
set -euo pipefail
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install sample-otel-app ./charts/sample-otel-app --namespace demo
kubectl -n demo get pods,svc
