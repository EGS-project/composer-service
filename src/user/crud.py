'''service.py module specific business logic'''

import json
from sqlalchemy.orm import Session
from src.auth.constants import GOOGLE, GITHUB

import src.user.models as models
import src.user.schemas as schemas
from src.user.constants import CONV_HISTORY_LIMIT
from user.utils import build_user_create

'''
use super_db;
show tables;
select * from users;
'''

def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_nickname(db: Session, nickname: str) -> models.User:
    return db.query(models.User).filter(models.User.nickname == nickname).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        email=user.email,
        premium=False,
        email_notification=True,
        whatsapp_notification=False,
        sms_notification=False,
        conv_history='[]')

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_conv_history(db: Session, db_user: models.User, item: str) -> models.User:
    conv_history_list: list[str] = json.loads(db_user.conv_history)
    conv_history_list.append(item)
    if not db_user.premium and len(conv_history_list) > CONV_HISTORY_LIMIT:
        conv_history_list.pop(0)
    updated_conv_history = json.dumps(conv_history_list)
    db_user.conv_history = updated_conv_history
    
    db.commit()
    db.refresh(db_user)
    return db_user


def get_or_create_user(db, userinfo: dict, auth_type: str) -> models.User:
    user = None
    if auth_type in [GOOGLE]:
        user = get_user_by_email(db=db, email=userinfo['email'])
    elif auth_type == GITHUB:
        user = get_user_by_nickname(db=db, email=userinfo['nickname'])
    if not user:
        user = create_user(
            db=db, user=build_user_create(userinfo=userinfo)
        )
    return user

