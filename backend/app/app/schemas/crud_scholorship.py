from pydantic import BaseModel
from typing import Optional

# CREATE
class CScholarship(BaseModel):
    token: str
    category: str
    deduction_percentage: float

# READ
class RScholarship(BaseModel):
    token: str
    id: Optional[int] = None

# UPDATE
class UScholarship(BaseModel):
    token: str
    id: int
    update_category: str
    update_deduction_percentage: float

# DELETE
class DScholarship(BaseModel):
    token: str
    id: int
