from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class Tearm(Base, Metadata):
    __tablename__ = "tearm"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300))

    class_subject=relationship("ClassSubject", back_populates="tearm")
    fees=relationship("Fees", back_populates="tearm")