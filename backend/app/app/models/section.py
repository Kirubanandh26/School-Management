from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class Section(Base, Metadata):
    __tablename__ = "section"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False, unique=True)
    
    classes = relationship("Classes", back_populates="section")

