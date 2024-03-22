import logging
import time

from fastapi import FastAPI, Request

from street_side_api.app.health import router as health_router
from street_side_api.app.v1.routing.router import router as v1_router

logger = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Steet Side API",
        description="API for the Street Side project",
        version="0.0.1",
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    app.include_router(health_router)
    app.include_router(v1_router)
    
    return app


app = create_app()
