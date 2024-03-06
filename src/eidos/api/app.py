import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
import structlog

from eidos import __version__
from eidos.api.routes.execution import router as router_execution
from eidos.api.routes.functions import router as router_functions
from eidos.settings import config

log = structlog.get_logger("eidos.api.app")

tags_metadata = [
    {
        "name": "health",
        "description": (
            "Health check endpoint. Useful for liveness and readiness probes."
        ),
    },
    {
        "name": "functions",
        "description": (
            "Operations with functions. "
            "Mainly listing and extracting the schema of functions."
        ),
    },
    {
        "name": "execution",
        "description": "Execution of functions.",
    },
]

app = FastAPI(
    title="eidos",
    description="API for the validation and execution of AI functions",
    version=__version__,
    root_path=config.root_path,
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/healthz", name="Health check", status_code=status.HTTP_200_OK, tags=["health"]
)
async def health():
    """
    Health check endpoint. Useful for liveness and readiness probes.
    """
    return Response(status_code=status.HTTP_200_OK)


app.include_router(router_execution, prefix="/api/v1/execution")
app.include_router(router_functions, prefix="/api/v1/functions")


def run_server():
    log.info(f"Deploying server at https://{config.api_host}:{config.api_port}")
    uvicorn.run(
        app,
        host=config.api_host,
        port=config.api_port,
        root_path=config.root_path,
        log_level=config.log_level,
    )
