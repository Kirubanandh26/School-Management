from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# CREATE
class CAttendance(BaseModel):
    token: str
    reg_no: str
    date: date
    attendance_status: int 
# READ
class RAttendance(BaseModel):
    token: str
    reg_no: Optional[str] = None


# UPDATE
class UAttendance(BaseModel):
    token: str
    id: int
    attendance_status: int


# DELETE
class DAttendance(BaseModel):
    token: str
    id: int
