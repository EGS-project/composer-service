'''router.py is a core of each module with all the endpoints'''

from http import HTTPStatus
from fastapi import APIRouter, Depends, Request, Response
from starlette.responses import RedirectResponse, JSONResponse
from src.auth.dependencies import Auth0
from src.auth.utils import decoded_value, expire_session_cookie, logout_auth0, set_session_cookie
from authlib.integrations.starlette_client import StarletteOAuth2App
from src.auth.dependencies import api_key_cookie

auth_router = APIRouter()

@auth_router.get('/api/v1/auth')
async def auth(request: Request, response: Response, auth_client: StarletteOAuth2App = Depends(Auth0.client)):
    token = await auth_client.authorize_access_token(request)
    if token:
        userinfo = token['userinfo'] # contains keys: email, given_name, family_name, nickname, picture (url)
        # TODO if user is new -> register
        userdata = {"id": -123123,"email": "abc@XYZ.com"} # TODO fetch user data from DB
        response = RedirectResponse(url='/')
        set_session_cookie(response=response, userdata=userdata)
    else:
        response = RedirectResponse(url='/')
    
    return response


@auth_router.get('/api/v1/login')
async def login(request: Request, auth_client : StarletteOAuth2App = Depends(Auth0.client)):
    redirect_uri = request.url_for('auth')
    response = await auth_client.authorize_redirect(request, redirect_uri) # redirects to auth client login page
    return response

@auth_router.get("/api/v1/logout")
async def logout(request: Request, response: Response, cookie: str = Depends(api_key_cookie)):
    response = logout_auth0(redirect_uri=request.url_for('homepage'))
    expire_session_cookie(response=response)

    return response   

@auth_router.get('/') 
async def homepage(cookie: str = Depends(api_key_cookie)):
    return JSONResponse(content=f'Decoded cookie: {decoded_value(cookie)}', status_code=HTTPStatus.OK)
