# Engineering Notes

## Design goals

This project demonstrates production-oriented thinking rather than simply showing framework syntax. The main design goals are repeatability, observability, testability, secure defaults and a clean separation between application and infrastructure concerns.

## Architecture decisions

### 1. FastAPI as the service boundary

FastAPI provides an explicit HTTP contract, OpenAPI documentation and lightweight middleware support. The API exposes operational endpoints separately from versioned application endpoints.

### 2. Container-first execution

The Docker image runs as a non-root user and contains only the runtime dependencies required by the service. This reduces configuration drift between developer and CI environments.

### 3. Health versus metrics

`/health` is intentionally simple and suitable for a liveness/readiness probe. `/metrics` is machine-oriented and consumed by Prometheus. Keeping these responsibilities separate makes operational tooling easier to reason about.

### 4. CI as a quality gate

The GitHub Actions workflow executes tests and compilation before building the container image. The pipeline therefore validates application correctness before producing a deployable artifact.

### 5. Infrastructure as an explicit layer

Docker Compose represents local multi-service infrastructure. Kubernetes manifests represent the next deployment abstraction. Prometheus and Grafana provide the observability layer.

## Reliability considerations

A production system would add:

- readiness checks that validate required dependencies;
- graceful shutdown and request timeouts;
- database connection pooling;
- retry and backoff policies only where operations are safe to retry;
- rate limiting;
- circuit breaking for remote dependencies;
- alerting based on service-level indicators;
- backup and restore procedures;
- disaster-recovery objectives;
- horizontal autoscaling based on workload signals.

## Security considerations

The repository avoids committing real secrets. Production hardening should include:

- secret management rather than environment files in source control;
- TLS termination;
- authentication and authorisation;
- dependency and container vulnerability scanning;
- restrictive network policies;
- non-root containers;
- minimal container images;
- audit logging;
- least-privilege service accounts.

## Observability model

The initial telemetry model follows three practical signals:

1. **Traffic** — request count and rate.
2. **Latency** — request duration.
3. **Errors** — HTTP status distribution.

This is a foundation for an SRE-style service-level monitoring strategy. OpenTelemetry can later add traces and correlated structured logs.

## Scaling path

The application can evolve from a single Docker Compose environment into a cloud-native platform:

```text
Docker Compose
      ↓
Kubernetes Deployment
      ↓
Helm packaging
      ↓
Managed database + managed cache
      ↓
Terraform-managed cloud infrastructure
      ↓
Observability + autoscaling + progressive delivery
```

## Portfolio evidence

This project demonstrates practical understanding of backend development, API design, containerisation, CI/CD, monitoring, infrastructure automation, Linux-oriented operational thinking and cloud-native architecture.
