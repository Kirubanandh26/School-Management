from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class Standard(Base, Metadata):
    __tablename__ = "standard"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False, unique=True)
    
    classes = relationship("Classes", back_populates="standard")
    exam_standard = relationship("ExamStandard", back_populates="standard")


