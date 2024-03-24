#!/bin/sh

set -eu

exec python \
    /opt/street-side/street-side-api/street_side_api/main.py \
    --host ${HOST} \
    --port ${PORT} \
    --log-config ${LOG_CONFIG} \
    --workers ${WORKERS}
