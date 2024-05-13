#!/bin/sh

set -eu

# echo "run db migration"
# /opt/street-side/street-side-api/docker/migrate -path /opt/street-side/street-side-api/database/migrations -database "$POSTGRES_DSN" -verbose up

exec /opt/street-side/street-side-api/.venv/bin/python \
    /opt/street-side/street-side-api/street_side_api/main.py \
    --host ${HOST} \
    --port ${PORT} \
    --reload ${RELOAD} \
    --log-config ${LOG_CONFIG} \
    --workers ${WORKERS}
