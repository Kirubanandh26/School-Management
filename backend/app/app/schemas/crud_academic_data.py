from pydantic import BaseModel
from typing import Optional


class CAcademicData(BaseModel):
    token: str
    reg_no: str
    year: int


class UAcademicData(BaseModel):
    token: str
    id: int
    year: Optional[int] = None


class RAcademicData(BaseModel):
    token: str
    id: Optional[int] = None
    reg_no: Optional[str] = None


class DAcademicData(BaseModel):
    token: str
    id: int
