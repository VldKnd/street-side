#!/bin/sh

set -eu

exec /opt/street-side/street-side-scrapper/.venv/bin/python \
    /opt/street-side/street-side-scrapper/street_side/v1/scrapper/core/main.py