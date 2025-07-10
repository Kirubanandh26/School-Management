from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata
from datetime import datetime, timedelta

class PasswordReset(Base, Metadata):
    __tablename__ = "password_reset"

    id = Column(Integer, primary_key=True)
    mail = Column(String(300), nullable=False)
    otp = Column(String(100), nullable=False)
    expires_at = Column(DateTime, nullable=False)
