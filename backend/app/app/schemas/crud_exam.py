from pydantic import BaseModel
from typing import Optional

# CREATE
class CExam(BaseModel):
    token: str
    name: str

# READ
class RExam(BaseModel):
    token: str
    id: Optional[int] = None

# UPDATE
class UExam(BaseModel):
    token: str
    id: int
    update_name: str

# DELETE
class DExam(BaseModel):
    token: str
    id: int
