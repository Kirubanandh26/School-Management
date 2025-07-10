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
@router.post("/assign_scholarship")
def assign_scholarship(request: CStudentScholarship, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can assign scholarships!"}

    target = db.query(User).filter(User.reg_no == request.reg_no, User.status == 1).first()
    if not target:
        return {"status": 0, "message": "Student not found!"}

    scholarship = db.query(Scholarship).filter(Scholarship.id == request.scholarship_id, Scholarship.status == 1).first()
    if not scholarship:
        return {"status": 0, "message": "Scholarship not found!"}

    existing = db.query(StudentScholarship).filter(StudentScholarship.user_id == target.id).first()
    if existing:
        return {"status": 0, "message": "Scholarship already assigned to this student!"}

    new_assignment = StudentScholarship(
        user_id=target.id,
        scholarship_id=scholarship.id,
        created_by=requester.id
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return {"status": 1, "message": "Scholarship assigned successfully!"}


#READ
@router.post("/read_student_scholarship")
def read_student_scholarship(request: RStudentScholarship, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    target = db.query(User).filter(User.reg_no == request.reg_no, User.status == 1).first()
    if not target:
        return {"status": 0, "message": "Student not found!"}

    scholarship = db.query(StudentScholarship).filter(StudentScholarship.user_id == target.id).first()
    if not scholarship:
        return {"status": 0, "message": "Scholarship record not found!"}

    return {"status": 1, "data": jsonable_encoder(scholarship)}


#UPDATE
@router.post("/update_student_scholarship")
def update_student_scholarship(request: UStudentScholarship, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can update student scholarship!"}

    target = db.query(User).filter(User.reg_no == request.reg_no, User.status == 1).first()
    if not target:
        return {"status": 0, "message": "Student not found!"}

    scholarship_record = db.query(StudentScholarship).filter(StudentScholarship.user_id == target.id).first()
    if not scholarship_record:
        return {"status": 0, "message": "Scholarship assignment not found!"}

    scholarship_record.scholarship_id = request.scholarship_id
    scholarship_record.modified_by = requester.id

    db.commit()
    db.refresh(scholarship_record)
    return {"status": 1, "message": "Student scholarship updated successfully!"}


#DELETE
@router.post("/drop_student_scholarship")
def drop_student_scholarship(request: DStudentScholarship, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can remove student scholarship!"}

    target = db.query(User).filter(User.reg_no == request.reg_no, User.status == 1).first()
    if not target:
        return {"status": 0, "message": "Student not found!"}

    scholarship_record = db.query(StudentScholarship).filter(StudentScholarship.user_id == target.id).first()
    if not scholarship_record:
        return {"status": 0, "message": "Scholarship assignment not found!"}

    db.delete(scholarship_record)
    db.commit()
    return {"status": 1, "message": "Student scholarship removed successfully!"}
