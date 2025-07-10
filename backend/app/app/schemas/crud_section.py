from pydantic import BaseModel
from typing import Optional

class CSection(BaseModel):
    token:str
    name:str

class RSection(BaseModel):
    token:str
    id:Optional[int]=None

class USection(BaseModel):
    token: str 
    id:int
    update_value:str


class DSection(BaseModel):
    token:str
    id:int