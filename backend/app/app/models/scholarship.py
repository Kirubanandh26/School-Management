from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class Scholarship(Base, Metadata):
    __tablename__ = "scholarship"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(300))
    deduction_percentage = Column(Float)

    student_scholarship = relationship("StudentScholarship", back_populates="scholarship")