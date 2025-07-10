from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token
from fastapi.encoders import jsonable_encoder

router = APIRouter()

#CREATE
@router.post("/create_class_subject")
def create_class_subject(request: CClassSubject, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 2:
        return {"status": 0, "message": "Only admin and principal can create class subjects!"}

    exists = db.query(ClassSubject).filter(
        ClassSubject.subject_id == request.subject_id,
        ClassSubject.staff_id == request.staff_id,
        ClassSubject.class_room_id == request.class_room_id,
        ClassSubject.tearm_id == request.tearm_id,
        ClassSubject.status == 1
    ).first()

    if exists:
        return {"status": 0, "message": "Class subject already exists!"}

    soft_deleted = db.query(ClassSubject).filter(
        ClassSubject.subject_id == request.subject_id,
        ClassSubject.staff_id == request.staff_id,
        ClassSubject.class_room_id == request.class_room_id,
        ClassSubject.tearm_id == request.tearm_id,
        ClassSubject.status == -1
    ).first()

    if soft_deleted:
        soft_deleted.status = 1
        soft_deleted.e_book = request.e_book
        soft_deleted.modified_by = requester.id
        db.commit()
        db.refresh(soft_deleted)
        return {"status": 1, "message": "Class subject reactivated successfully!"}

    new_class_subject = ClassSubject(
        subject_id=request.subject_id,
        staff_id=request.staff_id,
        class_room_id=request.class_room_id,
        tearm_id=request.tearm_id,
        e_book=request.e_book,
        created_by=requester.id
    )

    db.add(new_class_subject)
    db.commit()
    db.refresh(new_class_subject)

    return {"status": 1, "message": "Class subject created successfully!"}



#READ
@router.post("/read_class_subject")
def read_class_subject(request: RClassSubject, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 3:
        return {"status": 0, "message": "You are not authorized to view class subjects!"}

    def class_subject(cs):
        class_obj = db.query(ClassRoom).filter(ClassRoom.id == cs.class_room_id).first()
        subject_obj = db.query(Subject).filter(Subject.id == cs.subject_id).first()
        teacher_obj = db.query(User).filter(User.id == cs.staff_id).first()
        
        return {
            "id": cs.id,
            "class": class_obj.id,
            "subject": subject_obj.name,
            "teacher": teacher_obj.name,
            "status": cs.status
        }

    if request.id:
        cs = db.query(ClassSubject).filter(ClassSubject.id == request.id, ClassSubject.status == 1).first()
        if not cs:
            return {"status": 0, "message": "Class subject not found!"}
        return {"status": 1, "data": class_subject(cs)}

    all_cs = db.query(ClassSubject).filter(ClassSubject.status == 1).all()
    all_data = [class_subject(cs) for cs in all_cs]

    return {"status": 1, "data": all_data}



# UPDATE
@router.post("/update_class_subject")
def update_class_subject(request: UClassSubject, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 2:
        return {"status": 0, "message": "Only admin and principal can update class subjects!"}

    class_subject = db.query(ClassSubject).filter(ClassSubject.id == request.id, ClassSubject.status == 1).first()
    if not class_subject:
        return {"status": 0, "message": "Class subject not found!"}

    if request.subject_id is not None:
        subject = db.query(Subject).filter(Subject.id == request.subject_id, Subject.status == 1).first()
        if not subject:
            return {"status": 0, "message": "Invalid subject ID!"}
        class_subject.subject_id = request.subject_id

    if request.staff_id is not None:
        staff = db.query(User).filter(User.id == request.staff_id, User.status == 1).first()
        if not staff:
            return {"status": 0, "message": "Invalid staff ID!"}
        class_subject.staff_id = request.staff_id

    if request.class_room_id is not None:
        classroom = db.query(ClassRoom).filter(ClassRoom.id == request.class_room_id, ClassRoom.status == 1).first()
        if not classroom:
            return {"status": 0, "message": "Invalid classroom ID!"}
        class_subject.class_room_id = request.class_room_id

    if request.tearm_id is not None:
        term = db.query(Tearm).filter(Tearm.id == request.tearm_id, Tearm.status == 1).first()
        if not term:
            return {"status": 0, "message": "Invalid term ID!"}
        class_subject.tearm_id = request.tearm_id

    if request.e_book is not None:
        class_subject.e_book = request.e_book

    class_subject.modified_by = requester.id
    db.commit()
    db.refresh(class_subject)

    return {"status": 1, "message": "Class subject updated successfully!"}



# DELETE CLASS SUBJECT
@router.post("/drop_class_subject")
def drop_class_subject(request: DClassSubject, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 2:
        return {"status": 0, "message": "Only admin can delete class subjects!"}

    class_subject = db.query(ClassSubject).filter(ClassSubject.id == request.id, ClassSubject.status == 1).first()
    if not class_subject:
        return {"status": 0, "message": "Class subject not found or already deleted!"}

    class_subject.status = -1
    class_subject.modified_by = requester.id

    db.commit()
    db.refresh(class_subject)

    return {"status": 1, "message": "Class subject deleted successfully!"}
