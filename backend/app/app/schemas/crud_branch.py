from pydantic import BaseModel, EmailStr
from typing import Optional

class CBranch(BaseModel):
    token: str
    name: str
    location: str
    mobile: str
    mail: EmailStr
    pin_code: str

class UBranch(BaseModel):
    token: str
    id: int
    name: Optional[str] = None
    location: Optional[str] = None
    mobile: Optional[str] = None
    mail: Optional[EmailStr] = None
    pin_code: Optional[str] = None

class RBranch(BaseModel):
    token: str
    id: Optional[int] = None

class DBranch(BaseModel):
    token: str
    id: int
