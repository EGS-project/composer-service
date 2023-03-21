'''router.py is a core of each module with all the endpoints'''

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import JSONResponse
from src.database.dependencies import database
from src.user.dependencies import current_user
from src.user.models import User
from fastapi.encoders import jsonable_encoder
import src.user.schemas as schemas
import src.user.crud as crud
from sqlalchemy.orm import Session


user_router = APIRouter()


@user_router.get('/api/v1/users/{id}')
async def get_user(id: int, user: User = Depends(current_user)):
    return JSONResponse(content=jsonable_encoder(user), status_code=HTTPStatus.OK)


@user_router.post("/api/v1/users", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(database)):
    try:
        db_user = crud.create_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=e.__str__(),
        ) from e
    return db_user
