from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class StudentLibrary(Base, Metadata):
    __tablename__ = "student_library"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    library_id = Column(Integer, ForeignKey("library.id"))
    from_date = Column(Date)
    to_date = Column(Date)
    late_charge = Column(Float)
    paid_charge = Column(Float)

    user = relationship("User", backref="student_librarie", foreign_keys=[user_id])
    library = relationship("Library", back_populates="student_librarie")