from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class Exam(Base, Metadata):
    __tablename__ = "exam"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300))

    exam_standard = relationship("ExamStandard", back_populates="exam")

