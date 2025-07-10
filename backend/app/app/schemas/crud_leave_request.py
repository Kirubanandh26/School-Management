from pydantic import BaseModel
from typing import Optional
from datetime import date

# CREATE
class CLeaveRequest(BaseModel):
    token: str
    academic_id: int
    from_date: date
    till_date: date
    description: str
    attendance_status: str 


# READ
class RLeaveRequest(BaseModel):
    token: str
    reg_no: Optional[str] = None


# UPDATE
class ULeaveRequest(BaseModel):
    token: str
    id: int
    attendance_status: str  

# DELETE
class DLeaveRequest(BaseModel):
    token: str
    id: int
