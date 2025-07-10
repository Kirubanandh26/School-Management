from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .user import User
from .metadata import Metadata

class Classes(Base, Metadata):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    standard_id = Column(Integer, ForeignKey("standard.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("section.id"), nullable=False)
    name = Column(String(50))

    standard = relationship("Standard", back_populates="classes")
    section = relationship("Section", back_populates="classes")
    class_room = relationship("ClassRoom", back_populates="classes")