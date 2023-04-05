'''router.py is a core of each module with all the endpoints'''

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import JSONResponse
from src.database.dependencies import database
from src.user.models import User
from fastapi.encoders import jsonable_encoder
import src.user.schemas as schemas
from sqlalchemy.orm import Session


user_router = APIRouter()

