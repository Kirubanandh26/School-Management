from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token
from fastapi.encoders import jsonable_encoder


router = APIRouter()


#CREATE
@router.post("/create_class_room")
def create_class_room(request: CClassRoom, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can create class rooms!"}

    existing = db.query(ClassRoom).filter(
        ClassRoom.classes_id == request.classes_id,
        ClassRoom.branch_id == request.branch_id
    ).first()

    if existing:
        if existing.status == 1:
            return {"status": 0, "message": "ClassRoom already exists for this class and branch!"}
        else:
            existing.status = 1
            existing.modified_by = requester.id
            db.commit()
            db.refresh(existing)
            return {"status": 1, "message": "ClassRoom reactivated successfully!"}

    new_class_room = ClassRoom(
        classes_id=request.classes_id,
        branch_id=request.branch_id,
        created_by=requester.id
    )

    db.add(new_class_room)
    db.commit()
    db.refresh(new_class_room)

    return {"status": 1, "message": "ClassRoom created successfully!"}



#READ
@router.post("/read_class_room")
def read_class_room(request: RClassRoom, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 3:
        return {"status": 0, "message": "You are not authorized to view class rooms!"}

    if request.id:
        class_room = db.query(ClassRoom).filter(ClassRoom.id == request.id, ClassRoom.status == 1).first()
        if not class_room:
            return {"status": 0, "message": "ClassRoom not found!"}
        return {"status": 1, "data": {"id":class_room.id,"class_id":class_room.classes_id, "branch_id":class_room.branch_id}}

    all_class_rooms = db.query(ClassRoom).filter(ClassRoom.status == 1).all()
    return {"status": 1, "data": [{"id":i.id,"class":i.classes_id, "branch":i.branch_id} for i in all_class_rooms]}


#UPDATE
@router.post("/update_class_room")
def update_class_room(request: UClassRoom, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can update class rooms!"}

    class_room = db.query(ClassRoom).filter(ClassRoom.id == request.id, ClassRoom.status == 1).first()
    if not class_room:
        return {"status": 0, "message": "ClassRoom not found!"}

    class_room.classes_id = request.classes_id
    class_room.branch_id = request.branch_id
    class_room.modified_by = requester.id

    db.commit()
    db.refresh(class_room)

    return {"status": 1, "message": "ClassRoom updated successfully!"}


#DELETE
@router.post("/drop_class_room")
def drop_class_room(request: DClassRoom, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can delete class rooms!"}

    class_room = db.query(ClassRoom).filter(ClassRoom.id == request.id, ClassRoom.status == 1).first()
    if not class_room:
        return {"status": 0, "message": "ClassRoom not found or already deleted!"}

    class_room.status = -1
    class_room.modified_by = requester.id

    db.commit()
    db.refresh(class_room)

    return {"status": 1, "message": "ClassRoom deleted successfully!"}
