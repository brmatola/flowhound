# 🐕 FlowHound

Passive Network Traffic Monitor — Powered by pmacct, Kafka, Prometheus, Grafana

---

## Project Summary

FlowHound is a lightweight, fully containerized passive network monitoring stack.

It captures traffic flows from a switch port mirror, aggregates them via Kafka, exposes metrics to Prometheus, and visualizes top talkers in Grafana.

Current features:

- Top MACs by total traffic
- Top source IPs
- Top destination IPs
- Stacked area graphs
- Dynamic Top N
- Safe, reproducible stack via Docker Compose
- Read-only provisioned dashboards

---

## How to Use it

### Start (daemon mode):

```bash
docker-compose up -d
```

### Stop:

```bash
docker-compose down
```

### Update entire stack:

```bash
git pull
docker-compose pull
docker-compose up -d --build
```

### Logs

For the whole stack:

```bash
docker-compose logs -f
```

For a service (see `docker-compose.yml for service names):

```bash
docker-compose logs -f $SERVICE
```

### Customize Dashboards

If you wish to customize:

- Open Grafana -> FlowHound -> select dashboard
- Click "Save As" -> save to "My Dashboards"
- Edit
- Optionall export updated JSON -> commit to `grafana-dashboards/`

## ❤️ Contributing

PRs and issues welcome!
Future roadmap and contribution guidelines coming soon.