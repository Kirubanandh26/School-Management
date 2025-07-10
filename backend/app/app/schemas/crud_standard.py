from pydantic import BaseModel
from typing import Optional

class CStandard(BaseModel):
    token:str
    name:str   
        
class RStandard(BaseModel):
    token:str
    name:Optional[str]=None

class UStandard(BaseModel):
    token:str
    id:int
    update_value:str

class DStandard(BaseModel):
    token:str
    id:int
