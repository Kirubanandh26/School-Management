from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class ClassSubject(Base, Metadata):
    __tablename__ = "class_subject"

    id = Column(Integer, primary_key=True, autoincrement=True)
    e_book = Column(String(300))
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    class_room_id = Column(Integer, ForeignKey("class_room.id"), nullable=False)
    tearm_id = Column(Integer, ForeignKey("tearm.id"), nullable=False
                      )
    subject = relationship("Subject", back_populates="class_subject")
    staff = relationship("User", backref="class_subject", foreign_keys=[staff_id])
    class_room = relationship("ClassRoom", back_populates="class_subject")
    tearm = relationship("Tearm", back_populates="class_subject")
    class_time_table = relationship("ClassTimeTable", back_populates="class_subject")
