# Troubleshooting

## Check observability pods

```bash
kubectl -n observability get pods
```

## Check demo app

```bash
kubectl -n demo get pods,svc
```

## Check app metrics

```bash
kubectl -n demo port-forward svc/sample-otel-app 8080:80
curl http://127.0.0.1:8080/metrics
```

## Check Alloy

```bash
kubectl -n observability logs deploy/alloy
```

## Check Tempo

```bash
kubectl -n observability get svc | grep tempo
```

## Check Loki

```bash
kubectl -n observability get svc | grep loki
```
