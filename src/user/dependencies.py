'''dependencies.py - Dependency Injection for router.py'''

import json
from src.auth.schemas import SessionData
from src.auth.utils import decoded_value
from sqlalchemy.orm import Session

from http import HTTPStatus
from fastapi import Depends, HTTPException
from src.auth.dependencies import api_key_cookie
from src.database.dependencies import database
from src.user.repository import UserRepository
from src.user.factory import UserFactory
from src.user.manager import UserManager


def user_repository(database: Session = Depends(database)) -> UserRepository:
    return UserRepository(db=database)

def user_factory(user_repository: UserRepository = Depends(user_repository)) -> UserFactory:
    return UserFactory(user_repository=user_repository)

def user_manager(
    user_factory: UserFactory = Depends(user_factory),
    user_repository: UserRepository = Depends(user_repository)
    ) -> UserManager:
    
    return UserManager(user_factory=user_factory, user_repository=user_repository)
