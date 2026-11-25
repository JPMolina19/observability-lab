# Incident Postmortem - INC-001

## Incident Summary

Application availability incident detected in Observability Lab API.

The service became unavailable, triggering Prometheus monitoring alerts and Alertmanager critical notification routing.

---

## Incident Severity

SEV-1

---

## Impact

During the incident window, the API service was unavailable.

Users attempting to access the application would receive service failures.

Affected component:

- Observability Lab API

---

## Detection

The incident was automatically detected through Prometheus monitoring.

Alert triggered:

ApplicationDown

Condition:

up{job="observability-app"} == 0

The alert was routed through Alertmanager using:

severity="critical"

---

## Timeline

| Time | Event |
|---|---|
| T+00 | Application became unavailable |
| T+01 | Prometheus detected target failure |
| T+02 | ApplicationDown alert entered FIRING state |
| T+03 | Alertmanager received critical alert |
| T+05 | Application service restored |
| T+06 | Alert returned to RESOLVED |

---

## Root Cause

The application container was intentionally stopped as part of an incident simulation.

---

## Resolution

The application service was restarted:

docker start observability-app

The service recovered and monitoring returned to healthy state.

---

## Corrective Actions

Completed:

- Added Prometheus availability monitoring.
- Implemented Alertmanager routing.
- Created Grafana reliability dashboard.
- Added SLO monitoring.
- Implemented synthetic monitoring.
- Moved to a request-based SLO with multi-window, multi-burn-rate alerts.
- Deployed on Kubernetes with liveness/readiness probes, so a crashed app container is restarted automatically.

Future improvements:

- Integrate external notification channels.