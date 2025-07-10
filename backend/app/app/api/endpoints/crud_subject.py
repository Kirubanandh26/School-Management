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
@router.post("/create_subject")
def create_subject(request: CSubject, db: Session = Depends(get_db)):
    reg_no = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == reg_no).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can create subjects!"}

    existing = db.query(Subject).filter(Subject.sub_code == request.sub_code).first()

    if existing:
        if existing.status == 1:
            return {"status": 0, "message": "Subject already exists!"}
        else:
            existing.status = 1
            existing.modified_by = requester.id
            db.commit()
            db.refresh(existing)
            return {"status": 1, "message": "Subject reactivated successfully!"}

    new_subject = Subject(
        name=request.name,
        sub_code=request.sub_code,
        created_by=requester.id
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return {"status": 1, "message": "Subject created successfully!"}


#READ
@router.post("/read_subject")
def read_subject(request: RSubject, db: Session = Depends(get_db)):
    reg_no = verify_token(request.token, db)
    user = db.query(User).filter(User.reg_no == reg_no).first()

    if user.designation>3:
        return {"status": 0, "message": "You are not authorized to read subjects!"}

    if request.id:
        subject = db.query(Subject).filter(Subject.id == request.id, Subject.status == 1).first()
        if not subject:
            return {"status": 0, "message": "Subject not found!"}
        return {"status": 1, "data": {"id":subject.id,"subject":subject.name}}

    if request.sub_code:
        subject = db.query(Subject).filter(Subject.sub_code == request.sub_code, Subject.status == 1).first()
        if not subject:
            return {"status": 0, "message": "Subject not found!"}
        return {"status": 1, "data": {"id":subject.id,"subject":subject.name}}

    all_subjects = db.query(Subject).filter(Subject.status == 1).all()
    return {"status": 1, "data": [{"id":i.id,"name":i.name} for i in all_subjects]}


#UPDATE
@router.post("/update_subject")
def update_subject(request: USubject, db: Session = Depends(get_db)):
    reg_no = verify_token(request.token, db)
    user = db.query(User).filter(User.reg_no == reg_no).first()

    if user.designation != 1:
        return {"status": 0, "message": "Only admin can update subjects!"}

    subject = db.query(Subject).filter(Subject.id == request.id, Subject.status == 1).first()
    if not subject:
        return {"status": 0, "message": "Subject not found!"}

    if request.name:
        subject.name = request.name
        subject.modified_by = user.id
    if request.sub_code:
        subject.sub_code = request.sub_code
        subject.modified_by = user.id

    db.commit()
    db.refresh(subject)

    return {"status": 1, "message": "Subject updated successfully!"}


#DELETE
@router.post("/drop_subject")
def drop_subject(request: DSubject, db: Session = Depends(get_db)):
    reg_no = verify_token(request.token, db)
    user = db.query(User).filter(User.reg_no == reg_no).first()

    if user.designation != 1:
        return {"status": 0, "message": "Only admin can delete subjects!"}

    subject = db.query(Subject).filter(Subject.id == request.id, Subject.status == 1).first()
    if not subject:
        return {"status": 0, "message": "Subject not found or already deleted!"}

    subject.status = -1
    subject.modified_by = user.id

    db.commit()
    db.refresh(subject)
    return {"status": 1, "message": "Subject deleted successfully!"}
