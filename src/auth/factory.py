

from http import HTTPStatus
from fastapi import Request, Response
from src.auth.schemas import SessionData
from src.auth.utils import encoded_value
import src.user.models as models

import src.config as config

class ResponseFactory:
    def __init__(self) -> None:
        pass
    
    def auth_response(self, user: models.User) -> Response:
        response = Response(status_code=HTTPStatus.OK, content="Authorized.")
        response.set_cookie(
            key = config.APP_COOKIE_NAME,
            value = encoded_value(SessionFactory.create_session(user=user)),
            domain = config.APP_HOST,
            path = '/',
            samesite="none",    
            secure=True)
        
        return response
    
    
    def logout_response(self, response: Response) -> Response:
        response.delete_cookie(
            key = config.APP_COOKIE_NAME,
            domain = config.APP_HOST,
            path = '/',
            samesite = "none",
            secure=True)
        
        return response

class SessionFactory:

    @classmethod
    def create_session(cls, user: models.User) -> dict:
        return SessionData(
            user_id=user.id,
            user_identification=user.email or user.nickname,
            auth_type=user.auth_type,
        ).__dict__
