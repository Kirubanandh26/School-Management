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
@router.post("/create_branch")
def create_branch(request: CBranch, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can create branches!"}

    existing_name = db.query(Branch).filter(Branch.name == request.name).first()
    existing_mobile = db.query(Branch).filter(Branch.mobile == request.mobile).first()
    existing_mail = db.query(Branch).filter(Branch.mail == request.mail).first()

    if existing_name and existing_name.status == 1:
        return {"status": 0, "message": "Branch with this name already exists!"}
    if existing_mobile and existing_mobile.status == 1:
        return {"status": 0, "message": "Branch with this mobile number already exists!"}
    if existing_mail and existing_mail.status == 1:
        return {"status": 0, "message": "Branch with this email already exists!"}

    if existing_name and existing_name.status != 1:
        existing_name.status = 1
        existing_name.modified_by = requester.id
        db.commit()
        db.refresh(existing_name)
        return {"status": 1, "message": "Branch reactivated successfully!"}

    new_branch = Branch(
        name=request.name,
        location=request.location,
        mobile=request.mobile,
        mail=request.mail,
        pin_code=request.pin_code,
        created_by=requester.id if hasattr(Branch, "created_by") else None
    )

    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)

    return {"status": 1, "message": "Branch created successfully!"}



#READ
@router.post("/read_branch")
def read_branch(request: RBranch, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can view branches!"}

    if request.id:
        target = db.query(Branch).filter(Branch.id == request.id, Branch.status == 1).first()
        if not target:
            return {"status": 0, "message": "Branch not found!"}
        return {
            "status": 1,
            "data": {
                "id": target.id,
                "name": target.name,
                "location": target.location,
                "mobile": target.mobile,
                "mail": target.mail,
                "pin_code": target.pin_code
            }
        }

    branches = db.query(Branch).filter(Branch.status == 1).all()
    return {
        "status": 1,
        "data": [
            {
                "id": b.id,
                "name": b.name,
                "location": b.location,
                "mobile": b.mobile,
                "mail": b.mail,
                "pin_code": b.pin_code
            } for b in branches
        ]
    }



#UPDATE
@router.post("/update_branch")
def update_branch(request: UBranch, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    user = db.query(User).filter(User.reg_no == user_reg).first()

    if user.designation != 1:
        return {"status": 0, "message": "Only admin can update branches!"}

    branch = db.query(Branch).filter(Branch.id == request.id, Branch.status == 1).first()
    if not branch:
        return {"status": 0, "message": "Branch not found!"}

    for field in ["name", "location", "mobile", "mail", "pin_code"]:
        value = getattr(request, field)
        if value is not None:
            setattr(branch, field, value)

    if hasattr(branch, "modified_by"):
        branch.modified_by = user.id

    db.commit()
    db.refresh(branch)
    return {"status": 1, "message": "Branch updated successfully!"}



#DELETE
@router.post("/drop_branch")
def drop_branch(request: DBranch, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    user = db.query(User).filter(User.reg_no == user_reg).first()

    if user.designation != 1:
        return {"status": 0, "message": "Only admin can delete branches!"}

    branch = db.query(Branch).filter(Branch.id == request.id, Branch.status == 1).first()
    if not branch:
        return {"status": 0, "message": "Branch not found or already deleted!"}

    branch.status = -1

    if hasattr(branch, "modified_by"):
        branch.modified_by = user.id

    db.commit()
    db.refresh(branch)
    return {"status": 1, "message": "Branch deleted successfully!"}
