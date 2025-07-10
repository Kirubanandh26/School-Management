from pydantic import BaseModel, EmailStr

class RequestOtp(BaseModel):
    mail:EmailStr