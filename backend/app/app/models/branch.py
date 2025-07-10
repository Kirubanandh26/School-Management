from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base import Base
from .user import User
from .metadata import Metadata

class Branch(Base, Metadata):
    __tablename__ = "branch"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300))
    location = Column(String(300))
    mobile = Column(String(300))
    mail = Column(String(300))
    pin_code = Column(String(300))

    user=relationship("User", back_populates="branch", foreign_keys=[User.branch_id])
    class_room = relationship("ClassRoom", back_populates="branch")