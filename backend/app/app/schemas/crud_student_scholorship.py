from pydantic import BaseModel
from typing import Optional


class CStudentScholarship(BaseModel):
    token: str
    reg_no: str
    scholarship_id: int


class RStudentScholarship(BaseModel):
    token: str
    reg_no: str


class UStudentScholarship(BaseModel):
    token: str
    reg_no: str
    scholarship_id: int


class DStudentScholarship(BaseModel):
    token: str
    reg_no: str

