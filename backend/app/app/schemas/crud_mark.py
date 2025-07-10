from pydantic import BaseModel, Field
from typing import Optional


class TokenBase(BaseModel):
    token: str


# CREATE MARK
class CMark(TokenBase):
    mark: float
    exam_standard_id: int
    academic_data_id: int


# READ MARK
class RMark(TokenBase):
    reg_no: Optional[str] = None 


# UPDATE MARK
class UMark(TokenBase):
    id: int
    mark: float


# DELETE MARK
class DMark(TokenBase):
    id: int


# RESPONSE SCHEMA
class MarkResponse(BaseModel):
    exam_standard_id: int
    mark: float
    grade: str


# MARK STATS
class MarkStatsResponse(BaseModel):
    pass_percentage: float
    average_percentage: float
    total_students: int
