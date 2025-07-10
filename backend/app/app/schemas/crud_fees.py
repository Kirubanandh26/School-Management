from pydantic import BaseModel
from typing import Optional
from datetime import date

class CFees(BaseModel):
    token: str
    academic_id: int
    tearm_id: int
    total_fees: float
    paid_fees: float
    due_date: date
    late_charges: float

class UFees(BaseModel):
    token: str
    id: int
    academic_id: Optional[int] = None
    tearm_id: Optional[int] = None
    total_fees: Optional[float] = None
    paid_fees: Optional[float] = None
    due_date: Optional[date] = None
    late_charges: Optional[float] = None

class RFees(BaseModel):
    token: str
    id: Optional[int] = None
