from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class Mark(Base, Metadata):
    __tablename__ = "mark"
    id = Column(Integer, primary_key=True)
    mark = Column(Float)
    grade = Column(String(300))
    exam_standard_id = Column(Integer, ForeignKey("exam_standard.id"))
    academic_data_id = Column(Integer, ForeignKey("academic_data.id"))

    exam_standard = relationship("ExamStandard", back_populates="mark")
    academic_data = relationship("AcademicData", back_populates="mark")
