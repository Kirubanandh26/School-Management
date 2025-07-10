from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class Library(Base, Metadata):
    __tablename__ = "library"
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_name = Column(String(300))
    book_sino = Column(String(300))
    author = Column(String(300))
    department = Column(String(300))
    total_copies = Column(Integer)
    available_copies = Column(Integer)

    student_librarie = relationship("StudentLibrary", back_populates="library")