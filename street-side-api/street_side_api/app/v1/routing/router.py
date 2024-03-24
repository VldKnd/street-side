from fastapi import APIRouter

import street_side_api.app.v1.routing.endpoints.name
import street_side_api.app.v1.routing.endpoints.sleep

router = APIRouter(prefix="/v1", tags=["Street Side Version 1 API"])

router.add_api_route(
    "/name",
    endpoint=street_side_api.app.v1.routing.endpoints.name.get_name,
    methods=["GET"],
    description="Get name of the application",
)

router.add_api_route(
    "/sleep/",
    endpoint=street_side_api.app.v1.routing.endpoints.sleep.get_sleep,
    methods=["GET"],
    description="Sleep given number of seconds",
)