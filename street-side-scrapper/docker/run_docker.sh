docker run \
    --volume ./configuration:/opt/street-side/configuration \
    --volume ./datastore/storage:/opt/street-side/datastore/storage \
    --env STREET_SIDE_CONFIGURATION_PATH="/opt/street-side/configuration/docker_prod.json" \
    --network="street-side_default" \
    street-side-scrapper