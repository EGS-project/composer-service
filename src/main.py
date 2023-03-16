'''main.py is a root of the project, which inits the FastAPI app'''

from urllib.parse import quote_plus, urlencode
from fastapi import FastAPI
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from docs.dependencies import custom_openapi
from src.auth.router import auth_router
from src.conversion.router import conversion_router

import config

app = FastAPI(openapi_url="/api/v1/openapi.yaml")
app.openapi = custom_openapi

app.add_middleware(
    SessionMiddleware,
    secret_key=config.APP_SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
    allow_methods=["*"],
    allow_headers=["*"],
    )

app.include_router(router=auth_router)
app.include_router(router=conversion_router)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=config.APP_HOST,
        port=int(config.APP_PORT),
        reload=True,
        server_header=False,
        ssl_certfile="certs/composer_public_key.pem",
        ssl_keyfile="certs/composer_private_key.pem"
    )
