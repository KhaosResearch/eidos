import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from eidos import __version__
from eidos.api.routes.execute import router as router_execute
from eidos.api.routes.functions import router as router_functions
from eidos.logs import get_logger
from eidos.settings import config

logger = get_logger("eidos.api")


app = FastAPI(
    title="eidos API",
    description="Validation and execution of AI functions",
    version=__version__,
    root_path=config.root_path,
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


app.include_router(router_execute, prefix="/api/v1/execute")
app.include_router(router_functions, prefix="/api/v1/functions")


def run_server():
    logger.info(f"Deploying server at https://{config.api_host}:{config.api_port}")
    uvicorn.run(
        app,
        host=config.api_host,
        port=config.api_port,
        root_path=config.root_path,
        log_level=config.log_level,
    )
