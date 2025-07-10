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
@router.post("/create_tearm")
def create_tearm(request: CTearm, db: Session = Depends(get_db)):
    reg_no = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == reg_no).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can create tearms!"}

    existing = db.query(Tearm).filter(Tearm.name == request.name).first()

    if existing:
        if existing.status == 1:
            return {"status": 0, "message": "Tearm already exists!"}
        else:
            existing.status = 1
            existing.modified_by = requester.id
            db.commit()
            db.refresh(existing)
            return {"status": 1, "message": "Tearm reactivated successfully!"}

    new_tearm = Tearm(
        name=request.name,
        created_by=requester.id
    )

    db.add(new_tearm)
    db.commit()
    db.refresh(new_tearm)

    return {"status": 1, "message": "Tearm created successfully!"}


#READ
@router.post("/read_tearm")
def read_tearm(request: RTearm, db: Session = Depends(get_db)):
    reg_no = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == reg_no).first()

    if requester.designation > 3:
        return {"status": 0, "message": "You are not authorized to view tearms!"}

    if request.id:
        tearm = db.query(Tearm).filter(Tearm.id == request.id, Tearm.status == 1).first()
        if not tearm:
            return {"status": 0, "message": "Tearm not found!"}
        return {"status": 1, "data": {"id": tearm.id, "name": tearm.name}}

    if request.name:
        tearm = db.query(Tearm).filter(Tearm.name == request.name, Tearm.status == 1).first()
        if not tearm:
            return {"status": 0, "message": "Tearm not found!"}
        return {"status": 1, "data": {"id": tearm.id, "name": tearm.name}}

    all_tearms = db.query(Tearm).filter(Tearm.status == 1).all()
    return {
        "status": 1,
        "data": [{"id": t.id, "name": t.name} for t in all_tearms]
    }


#UPDATE
@router.post("/update_tearm")
def update_tearm(request: UTearm, db: Session = Depends(get_db)):
    reg_no = verify_token(request.token, db)
    user = db.query(User).filter(User.reg_no == reg_no).first()

    if user.designation != 1:
        return {"status": 0, "message": "Only admin can update tearms!"}

    tearm = db.query(Tearm).filter(Tearm.id == request.id, Tearm.status == 1).first()
    if not tearm:
        return {"status": 0, "message": "Tearm not found!"}

    tearm.name = request.update_name
    tearm.modified_by = user.id

    db.commit()
    db.refresh(tearm)

    return {"status": 1, "message": "Tearm updated successfully!"}


#DELETE
@router.post("/drop_tearm")
def drop_tearm(request: DTearm, db: Session = Depends(get_db)):
    reg_no = verify_token(request.token, db)
    user = db.query(User).filter(User.reg_no == reg_no).first()

    if user.designation != 1:
        return {"status": 0, "message": "Only admin can delete tearms!"}

    tearm = db.query(Tearm).filter(Tearm.id == request.id, Tearm.status == 1).first()
    if not tearm:
        return {"status": 0, "message": "Tearm not found or already deleted!"}

    tearm.status = -1
    tearm.modified_by = user.id

    db.commit()
    db.refresh(tearm)
    return {"status": 1, "message": "Tearm deleted successfully!"}