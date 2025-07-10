from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .user import User
from .metadata import Metadata

class ClassRoom(Base, Metadata):
    __tablename__ = "class_room"

    id = Column(Integer, primary_key=True, autoincrement=True)
    classes_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branch.id"), nullable=False)
    
    branch = relationship("Branch", back_populates="class_room")
    classes= relationship("Classes", back_populates="class_room")
    class_subject = relationship("ClassSubject", back_populates="class_room")
    