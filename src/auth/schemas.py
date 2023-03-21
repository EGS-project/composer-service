from pydantic import BaseModel, EmailStr

class SessionData(BaseModel):
    user_id: int
    user_email: EmailStr
    