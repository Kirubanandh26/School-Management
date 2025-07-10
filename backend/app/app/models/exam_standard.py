from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class ExamStandard(Base, Metadata):
    __tablename__ = "exam_standard"
    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exam.id"))
    standard_id = Column(Integer, ForeignKey("standard.id"))

    standard = relationship("Standard", back_populates="exam_standard")
    mark = relationship("Mark", back_populates="exam_standard")
    exam = relationship("Exam", back_populates="exam_standard")
