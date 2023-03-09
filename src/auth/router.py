'''router.py is a core of each module with all the endpoints'''

from http import HTTPStatus
from urllib.parse import quote_plus, urlencode
from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from src.auth.dependencies import Auth0
from authlib.integrations.starlette_client import StarletteOAuth2App

import config

auth_router = APIRouter()


@auth_router.get('/auth')
async def auth(request : Request, auth_client : StarletteOAuth2App = Depends(Auth0.client)):
    token = await auth_client.authorize_access_token(request)
    request.session['token'] = token
    return RedirectResponse(url='/', status_code=HTTPStatus.FOUND)


@auth_router.get('/login')
async def login(request : Request, auth_client : StarletteOAuth2App = Depends(Auth0.client)):
    redirect_uri = request.url_for('auth')
    return await auth_client.authorize_redirect(request, redirect_uri) # redirects to auth client login page


@auth_router.get("/logout")
async def logout(request : Request):
    request.session.clear()
    return RedirectResponse(
        url=f"https://{config.AUTH0_DOMAIN}/v2/logout?" 
        + urlencode(
            {
                "returnTo": request.url_for('homepage'),
                "client_id": config.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )
