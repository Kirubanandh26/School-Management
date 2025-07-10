from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class StudentScholarship(Base, Metadata):
    __tablename__ = "student_scholarship"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    scholarship_id = Column(Integer, ForeignKey("scholarship.id"))

    user = relationship("User", backref="student_scholarship", foreign_keys=[user_id])
    scholarship = relationship("Scholarship", back_populates="student_scholarship")