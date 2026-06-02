#!/usr/bin/env bash
set -euo pipefail
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add headlamp https://kubernetes-sigs.github.io/headlamp/
helm repo update
