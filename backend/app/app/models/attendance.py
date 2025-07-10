from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from db.base import Base
from .metadata import Metadata

class Attendance(Base, Metadata):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    academic_id = Column(Integer, ForeignKey("academic_data.id"))
    attendance_status = Column(TINYINT)
    reg_no = Column(String(50))

    academic_data = relationship("AcademicData", back_populates="attendance")

