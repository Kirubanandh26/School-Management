from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class LeaveRequest(Base, Metadata):
    __tablename__ = "leave_request"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    academic_id = Column(Integer, ForeignKey("academic_data.id"))
    from_date = Column(Date)
    till_date = Column(Date)
    description = Column(Text)
    approved_by = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", foreign_keys=[user_id], backref="leave_request")
    academic_data = relationship("AcademicData", back_populates="leave_request")
    approver = relationship("User", foreign_keys=[approved_by], backref="approved_leave")









