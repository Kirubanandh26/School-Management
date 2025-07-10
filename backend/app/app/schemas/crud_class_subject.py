from pydantic import BaseModel
from typing import Optional


class CClassSubject(BaseModel):
    token: str
    subject_id: int
    staff_id: int
    class_room_id: int
    tearm_id: int
    e_book: Optional[str]


class RClassSubject(BaseModel):
    token: str
    id: Optional[int] = None


class UClassSubject(BaseModel):
    token: str
    id: int
    subject_id: Optional[int] = None
    staff_id: Optional[int] = None
    class_room_id: Optional[int] = None
    tearm_id: Optional[int] = None
    e_book: Optional[str] = None


class DClassSubject(BaseModel):
    token: str
    id: int
