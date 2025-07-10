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
@router.post("/create_section")
def create_section(request: CSection, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    if request_user.designation != 1:
        return {"status": 0, "message": "Only admin is authorized to perform this action!"}

    section = db.query(Section).filter(Section.name == request.name).first()

    if section:
        if section.status == 1:
            return {"status": 0, "message": "Section already exists!"}
        else:
            section.status = 1
            section.modified_by = request_user.id
            db.commit()
            db.refresh(section)
            return {"status": 1, "message": "Section reactivated successfully!"}

    new_section = Section(
        name=request.name,
        created_by=request_user.id
    )

    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return {"status": 1, "message": "Section created successfully!"}




#READ
@router.post("/read_section")
def read_section(request: RSection, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    if request_user.designation == 4:
        return {"status": 0, "message": "Your not authorized to perform this action!"}

    if request.id:
        section = db.query(Section).filter(
            and_(Section.id == request.id, Section.status == 1)
        ).first()

        if not section:
            return {"status": 0, "message": "Section doesn't exist!"}

        return {"status": 1, "data": {"id":section.id,"standard":section.name}}

    all_sections = db.query(Section).filter(Section.status == 1).all()
    return {"status": 1, "data": [{"id":i.id,"name":i.name} for i in all_sections]}




#UPDATE
@router.post("/update_section")
def update_section(request: USection, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    if request_user.designation != 1:
        return {"status": 0, "message": "Only admin is authorized to perform this action!"}

    target_section = db.query(Section).filter(
        and_(Section.id == request.id, Section.status == 1)
    ).first()

    if not target_section:
        return {"status": 0, "message": "Section doesn't exist!"}

    existing = db.query(Section).filter(
        and_(Section.name == request.update_value, Section.status == 1)
    ).first()

    if existing:
        return {"status": 0, "message": "Another section with the new name already exists!"}

    target_section.name = request.update_value
    target_section.modified_by = request_user.id

    db.commit()
    db.refresh(target_section)

    return {"status": 1, "message": "Section updated successfully!"}




#DROP
@router.post("/drop_section")
def drop_section(request: RSection, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    if request_user.designation != 1:
        return {"status": 0, "message": "Only admin is authorized to perform this action!"}

    target_section = db.query(Section).filter(
        and_(Section.id == request.id, Section.status == 1)
    ).first()

    if not target_section:
        return {"status": 0, "message": "Section doesn't exist or already deleted!"}

    target_section.status = -1
    target_section.modified_by = request_user.id

    db.commit()
    db.refresh(target_section)

    return {"status": 1, "message": "Section deleted successfully!"}
