#!/bin/bash
set -e

# Create a bucket for external services if it doesn't already exist
if ! influx bucket list --name services >/dev/null 2>&1; then
  influx bucket create --name services --org "$DOCKER_INFLUXDB_INIT_ORG"
fi

# Retrieve bucket ID for token creation
SERVICE_BUCKET_ID=$(influx bucket list --name services | awk 'NR==2 {print $1}')

# Create a token with read/write access to the services bucket
influx auth create \
  --description services-token \
  --read-bucket "$SERVICE_BUCKET_ID" \
  --write-bucket "$SERVICE_BUCKET_ID" \
  --org "$DOCKER_INFLUXDB_INIT_ORG" \
  --json > /var/lib/influxdb2/services-token.json
