from pydantic import BaseModel
from typing import Optional


class CTearm(BaseModel):
    token: str
    name: str


class UTearm(BaseModel):
    token: str
    id: int
    update_name: str


class RTearm(BaseModel):
    token: str
    id: Optional[int] = None
    name: Optional[str] = None


class DTearm(BaseModel):
    token: str
    id: int
