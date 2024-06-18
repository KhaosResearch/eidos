from fastapi import HTTPException, Security
from fastapi.security import APIKeyQuery
from starlette.status import HTTP_403_FORBIDDEN

from eidos.settings import settings

api_key_query = APIKeyQuery(name="X-API-Key", auto_error=False)


def validate_api_key(api_key: str = Security(api_key_query)) -> str | None:
    if not api_key:
        return None
    if api_key == settings.api_key:
        return api_key
    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API key")


query_scheme = validate_api_key
