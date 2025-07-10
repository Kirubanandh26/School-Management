from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class Metadata:
    @declared_attr
    def created_by(cls):
        return Column(Integer, ForeignKey("user.id"), nullable=True)

    @declared_attr
    def modified_by(cls):
        return Column(Integer, ForeignKey("user.id"), nullable=True)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow)

    @declared_attr
    def modified_at(cls):
        return Column(DateTime, default=None, onupdate=datetime.utcnow)

    @declared_attr
    def status(cls):
        return Column(Integer, default=1)
    
    @declared_attr
    def created_by_user(cls):
        return relationship("User", foreign_keys=[cls.created_by], lazy="joined")

    @declared_attr
    def modified_by_user(cls):
        return relationship("User", foreign_keys=[cls.modified_by], lazy="joined")