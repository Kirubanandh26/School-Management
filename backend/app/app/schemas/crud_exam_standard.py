from pydantic import BaseModel
from typing import Optional

# CREATE
class CExamStandard(BaseModel):
    token: str
    exam_id: int
    standard_id: int

# READ
class RExamStandard(BaseModel):
    token: str
    id: Optional[int] = None  # Optional filtering by ID

# UPDATE
class UExamStandard(BaseModel):
    token: str
    id: int
    exam_id: int
    standard_id: int

# DELETE
class DExamStandard(BaseModel):
    token: str
    id: int
