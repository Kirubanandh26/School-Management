from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class Token(Base, Metadata):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_no = Column(String(50))
    token = Column(String(1000, collation='utf8mb4_bin'))
    