# A way to tell pydantic that the id field is optional.
from pydantic import BaseModel, validator, EmailStr


class User(BaseModel):
    email: EmailStr = ""
    nickname: str = ""
    auth_type: str = ""
    premium: bool = False
    email_notification: bool = True
    whatsapp_notification: bool = False
    sms_notification: bool = False
    profile_picture: str = ""
    conv_history: list[str] = []
    
    class Config:
        orm_mode = True

'''Create'''
class UserCreate(User):
    pass


'''Read'''
class UserRead(User):
    id: int
