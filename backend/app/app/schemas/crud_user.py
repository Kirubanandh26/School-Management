from pydantic import BaseModel, EmailStr, constr
from typing import Optional,Annotated
from datetime import date



#CREATE
class CreateDynamicData(BaseModel):
    classroom_id: Optional[int]
    roll_no: Optional[str]
    photo: Optional[str]
    mid: Optional[str]

class CreateUser(BaseModel):
    token:str
    designation: int
    reg_no: str
    password: str
    name: str
    dob: Optional[date] = None
    blood_group: Optional[str] = None
    gender: Optional[str] = None
    mail: Optional[EmailStr]
    mobile: Optional[Annotated[str,constr(min_length=10, max_length=15)]]
    address: Optional[str] = None
    pincode: Optional[str] = None
    aadhar_num: Optional[Annotated[str,constr(min_length=12, max_length=12)]]
    nationality: Optional[str] = None
    religion: Optional[str] = None
    community: Optional[str] = None
    mom_name: Optional[str] = None
    dad_name: Optional[str] = None
    parent_mobile: Optional[Annotated[str,constr(min_length=10, max_length=15)]] = None
    parent_occupation: Optional[str] = None
    annual_income: Optional[float] = None
    machine_id: Optional[int] = None
    branch_id: Optional[int] = None
    dynamic_data: Optional[CreateDynamicData]

    class Config:
        orm_mode = True



#GET
class GetUser(BaseModel):
    token:str
    reg_no:str
    required_field:Optional[str]=None
    


#UPDATE
class UpdateDynamicData(BaseModel):
    roll_no: Optional[str]
    photo: Optional[str]
    mid: Optional[str]
    classroom_id: Optional[int]

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    token: str 
    reg_no: str
    update_field: Optional[str] = None
    update_value: Optional[str] = None

    designation: Optional[int] = None
    reg_no: Optional[str] = None
    name: Optional[str] = None
    dob: Optional[date] = None
    blood_group: Optional[str] = None
    gender: Optional[str] = None
    mail: Optional[EmailStr] = None
    mobile: Optional [Annotated[str,constr(min_length=10, max_length=15)]] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    aadhar_num: Optional[Annotated[str,constr(min_length=12, max_length=12)]]
    nationality: Optional[str] = None
    religion: Optional[str] = None
    community: Optional[str] = None
    mom_name: Optional[str] = None
    dad_name: Optional[str] = None
    parent_mobile: Optional[Annotated[str,constr(min_length=10, max_length=15)]] = None
    parent_occupation: Optional[str] = None
    annual_income: Optional[float] = None
    machine_id: Optional[int] = None
    branch_id: Optional[int] = None
    dynamic_data: Optional[UpdateDynamicData]



#DELETE
class DropUser(BaseModel):
    token:str
    reg_no:str
