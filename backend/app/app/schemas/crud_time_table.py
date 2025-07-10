from pydantic import BaseModel
from typing import Optional

class CTimeTable(BaseModel):
    token: str
    day: str
    period_no: int

class RTimeTable(BaseModel):
    token: str
    id: Optional[int] = None

class UTimeTable(BaseModel):
    token: str
    id: int
    update_day: str
    update_period_no: int

class DTimeTable(BaseModel):
    token: str
    id: int