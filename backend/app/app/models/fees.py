from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class Fees(Base, Metadata):
    __tablename__ = "fees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    academic_id = Column(Integer, ForeignKey("academic_data.id"))
    tearm_id = Column(Integer, ForeignKey("tearm.id"))
    total_fees = Column(Float)
    paid_fees = Column(Float)
    due_date = Column(Date)
    late_charges = Column(Float)

    academic_data = relationship("AcademicData", back_populates="fees")
    tearm = relationship("Tearm", back_populates="fees")