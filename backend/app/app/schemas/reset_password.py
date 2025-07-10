from pydantic import BaseModel, EmailStr

class ResetPassword(BaseModel):
    otp:str
    new_password:str