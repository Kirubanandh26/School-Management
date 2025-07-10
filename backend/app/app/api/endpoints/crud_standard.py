from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token, is_allowed_to_manage, roles
from core.hashing import hash_password
from sqlalchemy import and_, or_


router = APIRouter()



#CREATE
@router.post("/create_standard")
def create_standard(request: CStandard, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    if request_user.designation != 1:
        return {"status": 0, "message": "Only admin is authorized to perform this action!"}

    standard = db.query(Standard).filter(Standard.name == request.name).first()

    if standard:
        if standard.status == 1:
            return {"status": 0, "message": "Standard already exists!"}
        else:
            standard.status = 1
            standard.modified_by = request_user.id
            db.commit()
            db.refresh(standard)
            return {"status": 1, "message": "Standard reactivated successfully!"}

    new_standard = Standard(
        name=request.name,
        created_by=request_user.id
    )

    db.add(new_standard)
    db.commit()
    db.refresh(new_standard)

    return {"status": 1, "message": "Standard created successfully!"}




#READ
@router.post("/read_standard")
def read_standard(request: RStandard, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    if request_user.designation == 4:
        return {"status": 0, "message": "Your not authorized to perform this action!"}

    if request.name:
        standard = db.query(Standard).filter(
            and_(Standard.name == request.name, Standard.status == 1)
        ).first()

        if not standard:
            return {"status": 0, "message": "Standard doesn't exist!"}

        return {"status": 1, "data": {"id":standard.id,"standard":standard.name}}

    all_standards = db.query(Standard).filter(Standard.status == 1).all()
    return {"status": 1, "data": [{"id":i.id,"name":i.name} for i in all_standards]}




#UPDATE
@router.post("/update_standard")
def update_standard(request: UStandard, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    if request_user.designation != 1:
        return {"status": 0, "message": "Only admin is authorized to perform this action!"}

    target_standard = db.query(Standard).filter(
        and_(Standard.name == request.id, Standard.status == 1)
    ).first()

    if not target_standard:
        return {"status": 0, "message": "Standard doesn't exist!"}

    existing = db.query(Standard).filter(
        and_(Standard.name == request.update_value, Standard.status == 1)
    ).first()

    if existing:
        return {"status": 0, "message": "Another standard with the new name already exists!"}

    target_standard.name = request.update_value
    target_standard.modified_by = request_user.id

    db.commit()
    db.refresh(target_standard)

    return {"status": 1, "message": "Standard updated successfully!"}




#DROP
@router.post("/drop_standard")
def drop_standard(request: RStandard, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    if request_user.designation != 1:
        return {"status": 0, "message": "Only admin is authorized to perform this action!"}

    target_standard = db.query(Standard).filter(
        and_(Standard.id == request.id, Standard.status == 1)
    ).first()

    if not target_standard:
        return {"status": 0, "message": "Standard doesn't exist or already deleted!"}

    target_standard.status = -1
    target_standard.modified_by = request_user.id

    db.commit()
    db.refresh(target_standard)

    return {"status": 1, "message": "Standard deleted successfully!"}