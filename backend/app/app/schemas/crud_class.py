from pydantic import BaseModel
from typing import Optional

class CClass(BaseModel):
    token: str
    standard_id: int
    section_id: int
    name: str

class RClass(BaseModel):
    token: str
    id: Optional[int] = None
    name: Optional[str] = None

class UClass(BaseModel):
    token: str
    id: int
    name: str

class DClass(BaseModel):
    token: str
    id: int
