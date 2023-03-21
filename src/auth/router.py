'''router.py is a core of each module with all the endpoints'''

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Request, Response, routing
from starlette.responses import RedirectResponse, JSONResponse
from src.auth.factory import ResponseFactory
from src.database.dependencies import database
from src.auth.dependencies import Auth0
from src.auth.utils import decoded_value, retrieve_auth_type
from authlib.integrations.starlette_client import StarletteOAuth2App
from src.auth.dependencies import api_key_cookie
from src.auth.utils import build_session_data
from sqlalchemy.orm import Session
import src.user.models as models
import src.user.crud as crud

auth_router = APIRouter()

@auth_router.get('/api/v1/auth')
async def auth(
    request: Request, 
    auth_client: Auth0 = Depends(Auth0), 
    db: Session = Depends(database),
    response_factory: ResponseFactory = Depends(ResponseFactory)
    ):
    token: dict = await auth_client.get_token(request)
    user: models.User = crud.get_or_create_user(
        db=db, 
        userinfo=token['userinfo'], 
        auth_type=retrieve_auth_type(token['userinfo']['sub'])
        )
    return response_factory.auth_response(user=user)


@auth_router.get('/api/v1/login')
async def login(
    request: Request, 
    auth_client: Auth0 = Depends(Auth0)
    ):
    
    return await auth_client.authorize_redirect(request, request.url_for('auth'))


@auth_router.get("/api/v1/logout")
async def logout(
    request: Request,
    auth_client: Auth0 = Depends(Auth0), 
    cookie: str = Depends(api_key_cookie),
    response_factory: ResponseFactory = Depends(ResponseFactory)
    ):
    
    return response_factory.logout_response(
        response=auth_client.logout_redirect(redirect_uri=request.url_for('homepage'))
        )   


@auth_router.get('/')
async def homepage(cookie: str = Depends(api_key_cookie)):
    return JSONResponse(content=f'Decoded cookie: {decoded_value(cookie)}', status_code=HTTPStatus.OK)
