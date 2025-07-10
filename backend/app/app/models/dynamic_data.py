from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from db.base import Base
from .metadata import Metadata


class DynamicData(Base, Metadata):
    __tablename__ = "dynamic_data"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    classroom_id = Column(Integer, ForeignKey("class_room.id"))
    roll_no = Column(String(300))
    photo = Column(String(300))
    mid = Column(String(300))

    user = relationship("User", backref="dynamic_data", foreign_keys=[user_id])
    classroom = relationship("ClassRoom", backref="dynamic_data")
    academic_data = relationship("AcademicData", back_populates="dynamic_data") 
