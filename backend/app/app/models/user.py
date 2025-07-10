from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from db.base import Base
from .metadata import Metadata

class User(Base, Metadata):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    designation = Column(TINYINT, nullable=False)
    reg_no = Column(String(300), unique=True)
    password = Column(String(300), nullable=False)
    name = Column(String(300), nullable=False)
    dob = Column(Date)
    blood_group = Column(String(300))
    gender = Column(String(300))
    mail = Column(String(300), unique=True)
    mobile = Column(String(300), unique=True)
    address = Column(String(300))
    pincode = Column(String(300))
    aadhar_num = Column(String(300), unique=True)
    nationality = Column(String(300))
    religion = Column(String(300))
    community = Column(String(300))
    mom_name = Column(String(300))
    dad_name = Column(String(300))
    parent_mobile = Column(String(300))
    parent_occupation = Column(String(300))
    annual_income = Column(Float)
    machine_id = Column(Integer)


    branch_id = Column(Integer, ForeignKey("branch.id"))
    branch = relationship("Branch", back_populates="user", foreign_keys=[branch_id])
    