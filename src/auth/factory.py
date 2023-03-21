

from http import HTTPStatus
from fastapi import Request, Response
from src.auth.utils import build_session_data, encoded_value
import src.user.models as models

import src.config as config

class ResponseFactory:
    def __init__(self) -> None:
        pass
    
    def auth_response(self, user: models.User) -> Response:
        response = Response(status_code=HTTPStatus.OK, content="Authorized.")
        response.set_cookie(
            key = config.APP_COOKIE_NAME,
            value = encoded_value(build_session_data(user=user)),
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
