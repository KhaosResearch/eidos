from fastapi import Depends
from fastapi.security import APIKeyQuery

from eidos.settings import settings


def validate_api_key(
    api_key: str = Depends(APIKeyQuery(name=settings.api_key, auto_error=False)),
):
    if settings.api_key is None:
        return True
    return api_key == settings.api_key


query_scheme = validate_api_key
