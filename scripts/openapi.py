import json

from eidos.api import app
from fastapi.openapi.utils import get_openapi

with open("openapi.json", "w") as f:
    json.dump(
        get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            summary=app.summary,
            description=app.description,
            routes=app.routes,
            servers=app.servers,
        ),
        f,
    )
