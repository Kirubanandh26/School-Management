from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token, is_allowed_to_manage, roles
from core.hashing import hash_password
from sqlalchemy import and_, or_


router = APIRouter()


@router.post("/create_class")
def create_class(request: CClass, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can create classes!"}

    existing = db.query(Classes).filter(
        Classes.standard_id == request.standard_id,
        Classes.section_id == request.section_id,
        Classes.name == request.name
    ).first()

    if existing:
        if existing.status == 1:
            return {"status": 0, "message": "Class already exists!"}
        else:
            existing.status = 1
            existing.modified_by = requester.id
            db.commit()
            db.refresh(existing)
            return {"status": 1, "message": "Class reactivated successfully!"}

    new_class = Classes(
        standard_id=request.standard_id,
        section_id=request.section_id,
        name=request.name,
        created_by=requester.id
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return {"status": 1, "message": "Class created successfully!"}



# READ CLASS
@router.post("/read_class")
def read_class(request: RClass, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 3:
        return {"status": 0, "message": "You are not authorized to view classes!"}

    if request.id:
        class_ = db.query(Classes).filter(Classes.id == request.id, Classes.status == 1).first()
        if not class_:
            return {"status": 0, "message": "Class not found!"}
        return {"status": 1, "data": {"id":class_.id,"class":class_.name}}

    if request.name:
        class_ = db.query(Classes).filter(Classes.name == request.name, Classes.status == 1).first()
        if not class_:
            return {"status": 0, "message": "Class not found!"}
        return {"status": 1, "data": {"id":class_.id,"class":class_.name}}

    classes = db.query(Classes).filter(Classes.status == 1).all()
    return {"status": 1, "data": [{"id":i.id,"name":i.name} for i in classes]}


# UPDATE CLASS
@router.post("/update_class")
def update_class(request: UClass, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can update classes!"}

    class_ = db.query(Classes).filter(Classes.id == request.id, Classes.status == 1).first()
    if not class_:
        return {"status": 0, "message": "Class not found!"}

    duplicate = db.query(Classes).filter(
        Classes.name == request.name,
        Classes.id != request.id,
        Classes.status == 1
    ).first()

    if duplicate:
        return {"status": 0, "message": "Another class with this name already exists!"}

    class_.name = request.name
    class_.modified_by = requester.id

    db.commit()
    db.refresh(class_)
    return {"status": 1, "message": "Class updated successfully!"}



# DELETE CLASS
@router.post("/drop_class")
def drop_class(request: DClass, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can delete classes!"}

    class_ = db.query(Classes).filter(Classes.id == request.id, Classes.status == 1).first()
    if not class_:
        return {"status": 0, "message": "Class not found or already deleted!"}

    class_.status = -1
    class_.modified_by = requester.id

    db.commit()
    db.refresh(class_)
    return {"status": 1, "message": "Class deleted successfully!"}
