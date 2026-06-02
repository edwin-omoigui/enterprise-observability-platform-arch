#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${BASE_URL:-http://127.0.0.1:8080}"
for i in $(seq 1 100); do
  curl -s "$BASE_URL/work" > /dev/null || true
  if [ $((i % 10)) -eq 0 ]; then
    curl -s "$BASE_URL/error" > /dev/null || true
  fi
  sleep 0.2
done
echo "Generated sample traffic."
