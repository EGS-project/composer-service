'''utils.py - non-business logic functions, e.g. response normalization, data enrichment, etc.'''

from http import HTTPStatus
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from jose import jwt
import config

users = {"dmontagu": {"password": "secret1"}, "tiangolo": {"password": "secret2"}}
cookie_sec = APIKeyCookie(name="session")


def get_current_user(session: str = Depends(cookie_sec)):
    try:
        payload = jwt.decode(session, config.APP_SECRET_KEY)
        user = users[payload["sub"]]
        return user
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Unprocessable entity."
        )

