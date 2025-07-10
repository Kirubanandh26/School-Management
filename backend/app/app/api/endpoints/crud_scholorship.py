from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token
from sqlalchemy import and_
from datetime import date
from fastapi.encoders import jsonable_encoder


router = APIRouter()


#CREATE
@router.post("/create_scholarship")
def create_scholarship(request: CScholarship, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can create scholarships!"}

    target = db.query(Scholarship).filter(Scholarship.category == request.category).first()

    if target:
        if target.status == 1:
            return {"status": 0, "message": "Scholarship with this category already exists!"}
        else:
            target.status = 1
            target.modified_by = requester.id
            db.commit()
            db.refresh(target)
            return {"status": 1, "message": "Scholarship reactivated successfully!"}

    new_scholarship = Scholarship(
        category=request.category,
        deduction_percentage=request.deduction_percentage,
        created_by=requester.id
    )

    db.add(new_scholarship)
    db.commit()
    db.refresh(new_scholarship)

    return {"status": 1, "message": "Scholarship created successfully!"}



#READ
@router.post("/read_scholarship")
def read_scholarship(request: RScholarship, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 3:
        return {"status": 0, "message": "You're not authorized to view scholarships!"}

    if request.id:
        target = db.query(Scholarship).filter(Scholarship.id == request.id, Scholarship.status == 1).first()
        if not target:
            return {"status": 0, "message": "Scholarship not found!"}
        return {
            "status": 1,
            "data": {
                "id": target.id,
                "category": target.category,
                "deduction_percentage": target.deduction_percentage
            }
        }

    all_entries = db.query(Scholarship).filter(Scholarship.status == 1).all()
    return {
        "status": 1,
        "data": [
            {
                "id": i.id,
                "category": i.category,
                "deduction_percentage": i.deduction_percentage
            } for i in all_entries
        ]
    }


# UPDATE
@router.post("/update_scholarship")
def update_scholarship(request: UScholarship, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can update scholarships!"}

    scholarship = db.query(Scholarship).filter(Scholarship.id == request.id, Scholarship.status == 1).first()
    if not scholarship:
        return {"status": 0, "message": "Scholarship not found!"}

    scholarship.category = request.update_category
    scholarship.deduction_percentage = request.update_deduction_percentage
    scholarship.modified_by = requester.id

    db.commit()
    db.refresh(scholarship)

    return {"status": 1, "message": "Scholarship updated successfully!"}


# DELETE
@router.post("/drop_scholarship")
def drop_scholarship(request: DScholarship, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can delete scholarships!"}

    scholarship = db.query(Scholarship).filter(Scholarship.id == request.id, Scholarship.status == 1).first()
    if not scholarship:
        return {"status": 0, "message": "Scholarship not found or already deleted!"}

    scholarship.status = -1
    scholarship.modified_by = requester.id

    db.commit()
    db.refresh(scholarship)

    return {"status": 1, "message": "Scholarship deleted successfully!"}
