'''router.py is a core of each module with all the endpoints'''

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import src.user.schemas as schemas
from src.database.dependencies import database
import src.user.models as models
from src.user.dependencies import current_user

user_router = APIRouter()

@user_router.get('/api/v1/user')
async def get_user(
    request: Request, 
    current_user: models.User = Depends(current_user)
    ):
    return schemas.UserRead.parse_obj(current_user.__dict__)
