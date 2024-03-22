#!/bin/sh

set -eu

exec /opt/street-side/street-side-api/.venv/bin/python \
    /opt/street-side/street-side-api/street_side_api/main.py \
    --host ${HOST} \
    --port ${PORT} \
    --reload ${RELOAD} \
    --log-config ${LOG_CONFIG} \
    --workers ${WORKERS}
