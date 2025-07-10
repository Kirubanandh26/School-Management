from pydantic import BaseModel
from typing import Optional

# CREATE
class CClassTimeTable(BaseModel):
    token: str
    time_table_id: int
    class_subject_id: int

# READ
class RClassTimeTable(BaseModel):
    token: str
    id: Optional[int] = None  # If provided, fetch specific entry

# UPDATE
class UClassTimeTable(BaseModel):
    token: str
    id: int
    time_table_id: int
    class_subject_id: int

# DELETE
class DClassTimeTable(BaseModel):
    token: str
    id: int
