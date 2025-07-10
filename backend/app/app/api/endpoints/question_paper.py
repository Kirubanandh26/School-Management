from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, File, UploadFile, Form
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import Optional
from app.db.session import get_db
from app.models.exam import Exam
from app.models.subject import Subject
from app.models.user import User
from app.models.mark import Mark
from app.models.classes import Classes
from app.models.question_paper import Question
from pydantic import BaseModel
from app.utils import file_storage
from app.core.config import settings

from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

router = APIRouter()


class QuestionPaperG(BaseModel):

    Exam: str
    subject: str
    classes_id:int


@router.post("/question_get", response_class=PlainTextResponse)
def qget(request: QuestionPaperG, db: Session = Depends(get_db)):
    log = db.query(Question).join(Exam, Exam.id==Question.exam_id).join(Subject, Subject.id==Question.subject_id).join(Classes, Classes.id==Question.classes_id).filter( and_(Exam.name.ilike(request.Exam), Subject.name.ilike(request.subject), Classes.id==request.classes_id)).first()

    if not log:
        raise HTTPException(status_code=401, detail="Not Found!")
    return log.question_url

@router.post("/question_post")
def qpost(question_file:UploadFile=File(...), exam_id:int=Form(...), classes_id:int=Form(...), subject_id:int=Form(...), db: Session = Depends(get_db)):
    full_path, relative_path=file_storage(question_file,question_file.filename)
    qp=Question(question_url=full_path, exam_id=exam_id, classes_id=classes_id, subject_id=subject_id, )

    db.add(qp)
    db.commit()
    return full_path


