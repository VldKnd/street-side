from fastapi import APIRouter

import street_side_api.app.v1.routing.endpoints.data
import street_side_api.app.v1.routing.endpoints.name
import street_side_api.app.v1.routing.endpoints.sleep

router = APIRouter(prefix="/v1", tags=["Street Side Version 1 API"])

router.add_api_route(
    "/list_companies",
    endpoint=street_side_api.app.v1.routing.endpoints.data.get_all_companies,
    methods=["GET"],
    description="Get the names of all the companies in the database",
)

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