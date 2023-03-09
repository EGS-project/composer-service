'''main.py is a root of the project, which inits the FastAPI app'''

from http import HTTPStatus
import json
from urllib.parse import quote_plus, urlencode
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import JSONResponse
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from src.auth.router import auth_router

import config

app = FastAPI(
    title="Converter Web App",
    description='Converter Web App',
    version="v1.0.0",
    terms_of_service="https://en.wikipedia.org/wiki/Terms_of_service",
    contact={
        "name": "Our GitHub organization",
        "url": "https://github.com/EGS-project"
    },
    license_info={
        "name": "Beerware License",
        "url": "https://en.wikipedia.org/wiki/Beerware",
    },)

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

@app.get('/')
async def homepage(request: Request):
    token = request.session.get('token')
    if token:
        message = {'message': f'Hello! Your token is: {json.dumps(token)}'}
        return JSONResponse(content=message, status_code=HTTPStatus.OK)
    else:
        return RedirectResponse(url='/login', status_code=HTTPStatus.SEE_OTHER)
    
app.include_router(router=auth_router)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=config.APP_HOST,
        port=int(config.APP_PORT),
        reload=True,
        server_header=False,
    )
