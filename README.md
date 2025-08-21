# SLA Infrastructure

Infrastructure for monitoring SLA violations with InfluxDB, Grafana and n8n.

## Quick start

Run services step by step.

### Step 1 – InfluxDB
```bash
docker compose up -d influxdb
curl -I http://localhost:8086/health
```
Default login: `admin` / `adminpassword`, token `admintoken`.

### Step 2 – Grafana
```bash
docker compose up -d grafana
curl -I http://localhost:3000/login
```
Default login: `admin` / `admin`.

### Step 3 – n8n
```bash
docker compose up -d n8n
curl -I http://localhost:5678
```
Open http://localhost:5678 in a browser to access the editor.

Data is stored in `influxdb/`, `grafana/`, `n8n/` and `local-files/`.
