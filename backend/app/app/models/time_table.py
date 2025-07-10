from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from db.base import Base
from .metadata import Metadata

class TimeTable(Base, Metadata):
    __tablename__ = "time_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(String(300))
    period_no = Column(TINYINT)

    class_time_table = relationship("ClassTimeTable", back_populates="time_table")
