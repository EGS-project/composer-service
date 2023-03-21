'''models.py for db models'''

import json
from sqlalchemy import ARRAY, JSON, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    nickname = Column(String(50), default="")
    auth_type = Column(String(20), default="")
    premium = Column(Boolean, default=False)
    email_notification = Column(Boolean, default=True)
    whatsapp_notification = Column(Boolean, default=False)
    sms_notification = Column(Boolean, default=False)
    profile_picture = Column(String(1024), default="")
    conv_history = Column(Text(length='mediumtext'), default='[]')
