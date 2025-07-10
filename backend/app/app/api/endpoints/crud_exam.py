from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token, is_allowed_to_manage, roles
from core.hashing import hash_password
from sqlalchemy import and_, or_
from fastapi.encoders import jsonable_encoder


router = APIRouter()


#CREATE
@router.post("/create_exam")
def create_exam(request: CExam, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can create exam!"}

    existing = db.query(Exam).filter(Exam.name == request.name).first()
    if existing:
        if existing.status == 1:
            return {"status": 0, "message": "Exam already exists!"}
        else:
            existing.status = 1
            existing.modified_by = requester.id
            db.commit()
            db.refresh(existing)
            return {"status": 1, "message": "Exam reactivated successfully!"}

    new_exam = Exam(
        name=request.name,
        created_by=requester.id
    )

    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    return {"status": 1, "message": "Exam created successfully!"}



#READ
@router.post("/read_exam")
def read_exam(request: RExam, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 3:
        return {"status": 0, "message": "You're not authorized to view exams!"}

    if request.id:
        exam = db.query(Exam).filter(Exam.id == request.id, Exam.status == 1).first()
        if not exam:
            return {"status": 0, "message": "Exam not found!"}
        return {"status": 1, "data": {"id": exam.id, "name": exam.name}}

    exams = db.query(Exam).filter(Exam.status == 1).all()
    return {"status": 1, "data": [{"id": e.id, "name": e.name} for e in exams]}



#UPDATE
@router.post("/update_exam")
def update_exam(request: UExam, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can update exam!"}

    exam = db.query(Exam).filter(Exam.id == request.id, Exam.status == 1).first()
    if not exam:
        return {"status": 0, "message": "Exam not found!"}

    exam.name = request.update_name
    exam.modified_by = requester.id

    db.commit()
    db.refresh(exam)

    return {"status": 1, "message": "Exam updated successfully!"}



#DELETE
@router.post("/drop_exam")
def drop_exam(request: DExam, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can delete exam!"}

    exam = db.query(Exam).filter(Exam.id == request.id, Exam.status == 1).first()
    if not exam:
        return {"status": 0, "message": "Exam not found or already deleted!"}

    exam.status = -1
    exam.modified_by = requester.id

    db.commit()
    db.refresh(exam)

    return {"status": 1, "message": "Exam deleted successfully!"}
