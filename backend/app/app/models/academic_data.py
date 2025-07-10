from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class AcademicData(Base, Metadata):
    __tablename__ = "academic_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    year = Column(Integer)
    dynamic_data_id = Column(Integer, ForeignKey("dynamic_data.id"))

    user = relationship("User", backref="academic_data", foreign_keys=[user_id])
    dynamic_data = relationship("DynamicData", back_populates="academic_data")
    mark = relationship("Mark", back_populates="academic_data")
    attendance = relationship("Attendance", back_populates="academic_data")
    leave_request = relationship("LeaveRequest", back_populates="academic_data")
    fees = relationship("Fees", back_populates="academic_data")