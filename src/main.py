'''main.py is a root of the project, which inits the FastAPI app'''

from http import HTTPStatus
import json
from urllib.parse import quote_plus, urlencode
from fastapi import APIRouter, Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, HTMLResponse
from authlib.integrations.starlette_client import OAuth

import config

app = FastAPI()
app.add_middleware(
    SessionMiddleware, 
    secret_key=config.APP_SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    
oauth = OAuth()
oauth.register(
    name='auth0',
    client_id=config.AUTH0_CLIENT_ID,
    client_secret=config.AUTH0_CLIENT_SECRET,
    api_base_url=config.AUTH0_DOMAIN,
    access_token_url=f'https://{config.AUTH0_DOMAIN}/oauth/token',
    authorize_url=f'https://{config.AUTH0_DOMAIN}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{config.AUTH0_DOMAIN}/.well-known/openid-configuration',
)


# Controllers API
@app.route('/')
async def homepage(request):
    token = request.session.get('token')
    if token:
        user = request.session.get('user')
        message = {'message': f'Hello! Your token is: {json.dumps(token)}'}
        return JSONResponse(content=message, status_code=HTTPStatus.OK)
    else:
        return RedirectResponse(url='/login', status_code=HTTPStatus.TEMPORARY_REDIRECT)


@app.route('/auth', methods=["GET", "POST"])
async def auth(request):
    token = await oauth.auth0.authorize_access_token(request)
    request.session['token'] = token
    return RedirectResponse(url='/', status_code=HTTPStatus.TEMPORARY_REDIRECT)


@app.route('/login')
async def login(request):
    redirect_uri = request.url_for('auth')
    return await oauth.auth0.authorize_redirect(request, redirect_uri) # redirects to auth0 login page


@app.route("/logout")
async def logout(request: Request):
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
    

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=config.APP_HOST,
        port=int(config.APP_PORT),
        reload=True,
        server_header=False,
    )
