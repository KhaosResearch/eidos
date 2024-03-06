import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from eidos import __version__
from eidos.routes.execution import router as router_execution
from eidos.routes.functions import router as router_functions
from eidos.settings import settings

log = structlog.get_logger("app")

openapi_tags = [
    {
        "name": "health",
        "description": (
            "Health check endpoint. Useful for liveness and readiness probes."
        ),
    },
    {
        "name": "functions",
        "description": "View and validate functions schema.",
    },
    {
        "name": "execution",
        "description": "Run functions as a service.",
    },
]

app = FastAPI(
    title="eidos",
    description="Function calling framework for LLMs.",
    version=__version__,
    root_path=settings.root_path,
    openapi_tags=openapi_tags,
    docs_url="/api/docs",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthCheckResponse(BaseModel):
    status: str


@app.get("/healthz", tags=["health"], response_model=HealthCheckResponse)
def health():
    """
    Health check endpoint. Useful for liveness and readiness probes.
    """
    return {"status": "ok"}


app.include_router(router_execution, prefix="/api/v1/execution")
app.include_router(router_functions, prefix="/api/v1/functions")
