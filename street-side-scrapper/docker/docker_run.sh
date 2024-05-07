docker run \
    --volume ./datastore/storage:/opt/street-side/datastore/storage \
    --env SCRAPPER_CONFIGURATION_PATH="/opt/street-side/street-side-scrapper/configurations/all.json" \
    --env STREET_SIDE_DATASTORE_PATH="/opt/street-side/datastore/storage" \
    --env POSTGRES_DSN="postgresql://postgres:postgres@postgres:5432/street-side?sslmode=disable" \
    --network="street-side_default" \
    street-side-scrapper-worker
