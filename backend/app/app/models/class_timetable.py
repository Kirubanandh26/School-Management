from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class ClassTimeTable(Base, Metadata):
    __tablename__ = "class_time_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_table_id = Column(Integer, ForeignKey("time_table.id"))
    class_subject_id = Column(Integer, ForeignKey("class_subject.id"))

    time_table = relationship("TimeTable", back_populates="class_time_table")
    class_subject = relationship("ClassSubject", back_populates="class_time_table")