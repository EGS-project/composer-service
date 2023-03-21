'''utils.py - non-business logic functions, e.g. response normalization, data enrichment, etc.'''
import src.user.schemas as schemas


def build_user_create(userinfo: dict) -> schemas.UserCreate:
    return schemas.UserCreate(
        email=userinfo['email'],
        premium=False,
        email_notification=True,
        whatsapp_notification=False,
        sms_notification=False,
        conv_history=[],
    )
