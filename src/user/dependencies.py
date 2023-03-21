'''dependencies.py - Dependency Injection for router.py'''

from src.auth.utils import decoded_value

from http import HTTPStatus
from fastapi import Depends, HTTPException
from src.auth.dependencies import api_key_cookie

def current_user(cookie: str = Depends(api_key_cookie)):
    try:
        return decoded_value(cookie)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Unprocessable entity.",
        ) from e
