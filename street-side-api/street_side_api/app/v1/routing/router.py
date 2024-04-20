from fastapi import APIRouter
from fastapi.responses import FileResponse

import street_side_api.app.v1.routing.endpoints.data
import street_side_api.app.v1.routing.endpoints.name
import street_side_api.app.v1.routing.endpoints.sleep

router = APIRouter(prefix="/v1", tags=["Street Side Version 1 API"])

router.add_api_route(
    "/download_file/{document_hash_id}",
    endpoint=street_side_api.app.v1.routing.endpoints.data.download_file_by_document_hash_id,
    methods=["GET"],
    response_class=FileResponse,
    description="Download file stored for document",
)

router.add_api_route(
    "/get_file_as_base64_by_document_hash_id/{document_hash_id}",
    endpoint=street_side_api.app.v1.routing.endpoints.data.get_file_as_base64_by_document_hash_id,
    methods=["GET"],
    description="Get the file stored for document",
)

router.add_api_route(
    "/get_documents_by_document_type_hash_id/{document_type_hash_id}",
    endpoint=street_side_api.app.v1.routing.endpoints.data.get_documents_by_document_type_hash_id,
    methods=["GET"],
    description="Get of all the document of give type",
)

router.add_api_route(
    "/get_document_types_by_company_hash_id/{company_hash_id}",
    endpoint=street_side_api.app.v1.routing.endpoints.data.get_document_types_by_company_hash_id,
    methods=["GET"],
    description="Get of all the document types of give company",
)

router.add_api_route(
    "/get_all_companies",
    endpoint=street_side_api.app.v1.routing.endpoints.data.get_all_companies,
    methods=["GET"],
    description="Get of all the companies in the database",
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