from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .metadata import Metadata

class QuestionPaper(Base, Metadata):
    __tablename__ = "question_paper"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_url = Column(String(1000))
    exam_id = Column(Integer, ForeignKey("exam.id"), nullable=False)
    class_subject_id = Column(Integer, ForeignKey("class_subject.id"), nullable=False)

    class_subject = relationship("ClassSubject", backref="question_paper")
    exam = relationship("Exam", backref="question_paper")
   