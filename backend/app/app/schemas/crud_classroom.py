from pydantic import BaseModel
from typing import Optional


class CClassRoom(BaseModel):
    token: str
    classes_id: int
    branch_id: int


class RClassRoom(BaseModel):
    token: str
    id: Optional[int] = None


class UClassRoom(BaseModel):
    token: str
    id: int
    classes_id: int
    branch_id: int


class DClassRoom(BaseModel):
    token: str
    id: int
    