from fastapi.security import APIKeyQuery

from fastapi import Depends

from eidos.settings import config as settings


def validate_api_key(
    api_key: str = Depends(APIKeyQuery(name=settings.api_key, auto_error=False)),
):
    if settings.api_key is None:
        return True
    return api_key == settings.api_key


get_api_key = validate_api_key
