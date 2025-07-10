from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class Subject(Base, Metadata):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False, unique=True)      
    sub_code = Column(String(300), nullable=False, unique=True) 
    
    class_subject = relationship("ClassSubject", back_populates="subject")
