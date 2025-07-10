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
@router.post("/create_academic_data")
def create_academic_data(request: CAcademicData, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.id>2:
        return {"status": 0, "message": "Your are not allowed to create academic data!"}

    target_user = db.query(User).filter(User.reg_no == request.reg_no, User.status == 1).first()
    if not target_user:
        return {"status": 0, "message": "Target user not found!"}

    dynamic_data = db.query(DynamicData).filter(DynamicData.user_id == target_user.id).first()
    if not dynamic_data:
        return {"status": 0, "message": "Dynamic data not found for the target user!"}

    existing = db.query(AcademicData).filter(
        AcademicData.user_id == target_user.id,
        AcademicData.year == request.year,
        AcademicData.status == 1
    ).first()
    if existing:
        return {"status": 0, "message": "Academic data for this year already exists!"}

    academic_data = AcademicData(
        user_id=target_user.id,
        year=request.year,
        dynamic_data_id=dynamic_data.id,
        created_by=requester.id if hasattr(AcademicData, "created_by") else None
    )
    db.add(academic_data)
    db.commit()
    db.refresh(academic_data)

    return {"status": 1, "message": "Academic data created successfully!"}




#READ
@router.post("/read_academic_data")
def read_academic_data(request: RAcademicData, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    user = db.query(User).filter(User.reg_no == user_reg).first()

    if user.designation > 3:
        return {"status": 0, "message": "Only Admin, Principal, or Teacher can view academic data!"}

    if request.id:
        academic = db.query(AcademicData).filter(
            AcademicData.id == request.id,
            AcademicData.status == 1
        ).first()

        if not academic:
            return {"status": 0, "message": "Academic data not found!"}

        return {
            "status": 1,
            "data": {
                "id": academic.id,
                "user_id": academic.user_id,
                "year": academic.year,
                "dynamic_data_id": academic.dynamic_data_id
            }
        }

    if request.reg_no:
        target = db.query(User).filter(User.reg_no == request.reg_no).first()
        if not target:
            return {"status": 0, "message": "Target user not found!"}

        records = db.query(AcademicData).filter(
            AcademicData.user_id == target.id,
            AcademicData.status == 1
        ).all()

        return {
            "status": 1,
            "data": [
                {
                    "id": i.id,
                    "user_id": i.user_id,
                    "year": i.year,
                    "dynamic_data_id": i.dynamic_data_id
                } for i in records
            ]
        }

    all_data = db.query(AcademicData).filter(AcademicData.status == 1).all()
    return {
        "status": 1,
        "data": [
            {
                "id": i.id,
                "user_id": i.user_id,
                "year": i.year,
                "dynamic_data_id": i.dynamic_data_id
            } for i in all_data
        ]
    }



#UPDATE
@router.post("/update_academic_data")
def update_academic_data(request: UAcademicData, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    updater = db.query(User).filter(User.reg_no == requester_reg).first()

    if updater.id>2:
        return {"status": 0, "message": "Only admin and principal can update academic data!"}

    academic = db.query(AcademicData).filter(AcademicData.id == request.id, AcademicData.status == 1).first()
    if not academic:
        return {"status": 0, "message": "Academic data not found!"}

    academic.year = request.year
    academic.modified_by = updater.id

    db.commit()
    db.refresh(academic)
    return {"status": 1, "message": "Academic data updated successfully!"}



#DELETE
@router.post("/drop_academic_data")
def drop_academic_data(request: DAcademicData, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    deleter = db.query(User).filter(User.reg_no == user_reg).first()

    if deleter.id>2:
        return {"status": 0, "message": "Your not accessed to delete academic data!"}

    academic = db.query(AcademicData).filter(AcademicData.id == request.id, AcademicData.status == 1).first()
    if not academic:
        return {"status": 0, "message": "Academic data not found or already deleted!"}

    academic.status = -1
    academic.modified_by = deleter.id

    db.commit()
    db.refresh(academic)
    return {"status": 1, "message": "Academic data deleted successfully!"}
