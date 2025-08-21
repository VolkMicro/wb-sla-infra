# SLA Infrastructure

Infrastructure for monitoring SLA violations with InfluxDB, Grafana, n8n and Traefik.

## Quick start

1. Copy environment file and adjust values:
   ```bash
   cp .env.example .env
   ```

2. Run services step by step.

### Step 1 – InfluxDB
```bash
docker compose up -d influxdb
curl -I http://localhost:8086/health
```

### Step 2 – Grafana
```bash
docker compose up -d grafana
curl -I http://localhost:3000/login
```

### Step 3 – n8n
```bash
docker compose up -d n8n
curl -I http://localhost:5678
```

### Step 4 – Traefik (HTTPS)
Add `DOMAIN_NAME`, `SUBDOMAIN` and `SSL_EMAIL` to `.env`.
```bash
docker compose up -d traefik
```
After DNS is configured, open `https://$SUBDOMAIN.$DOMAIN_NAME`.

Data is stored in `influxdb/`, `grafana/`, `n8n/`, `local-files/` and `letsencrypt/`.
