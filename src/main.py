'''main.py is a root of the project, which inits the FastAPI app'''

from fastapi import FastAPI
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from src.activemq.dependencies import activemq_worker_manager
from src.database.dependencies import db_engine
from docs.dependencies import custom_openapi
from src.auth.router import auth_router
from src.conversion.router import conversion_router
from src.user.router import user_router
from src.healthcheck.router import healthcheck_router
import src.user.models as user_models
import src.config as config


app = FastAPI(openapi_url="/api/v1/openapi.yaml")
# app.openapi = custom_openapi

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


@app.on_event("startup")
def startup_event() -> None:
    user_models.Base.metadata.create_all(bind=db_engine)
    activemq_worker_manager.submit_threadpool()
    
@app.on_event("shutdown")
def shutdown_event() -> None:
    # user_models.Base.metadata.drop_all(bind=db_engine)
    activemq_worker_manager.stop_threadpool()

        
    
app.include_router(router=auth_router)
app.include_router(router=user_router)
app.include_router(router=healthcheck_router)
app.include_router(router=conversion_router)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=config.APP_HOST,
        port=int(config.APP_PORT),
        reload=True,
        # server_header=False,
        # ssl_certfile="certs/composer_public_key.pem",
        # ssl_keyfile="certs/composer_private_key.pem"
    )
