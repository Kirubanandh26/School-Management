from pydantic import BaseModel
from typing import Optional

class Login(BaseModel):
    reg_no:str
    password:str



