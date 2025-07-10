from pydantic import BaseModel
from typing import Optional


class CSubject(BaseModel):
    token: str
    name: str
    sub_code: str


class USubject(BaseModel):
    token: str
    id: int
    name: Optional[str] = None
    sub_code: Optional[str] = None


class RSubject(BaseModel):
    token: str
    sub_code: Optional[str] = None
    id: Optional[int] = None


class DSubject(BaseModel):
    token: str
    id: int
