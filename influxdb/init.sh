#!/bin/bash
set -e
# Initialize InfluxDB bucket for SLA metrics
influx bucket create \
  --name "$DOCKER_INFLUXDB_INIT_BUCKET" \
  --org "$DOCKER_INFLUXDB_INIT_ORG" \
  --retention 30d || true
