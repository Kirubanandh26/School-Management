from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# CREATE
@router.post("/create_class_time_table")
def create_class_time_table(request: CClassTimeTable, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation >2:
        return {"status": 0, "message": "Only admin can create class time table entries!"}

    exists = db.query(ClassTimeTable).filter(
        ClassTimeTable.time_table_id == request.time_table_id,
        ClassTimeTable.class_subject_id == request.class_subject_id,
        ClassTimeTable.status == 1
    ).first()

    if exists:
        return {"status": 0, "message": "Class time table entry already exists!"}

    new_entry = ClassTimeTable(
        time_table_id=request.time_table_id,
        class_subject_id=request.class_subject_id,
        created_by=requester.id
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {"status": 1, "message": "Class time table entry created successfully!"}


# READ
@router.post("/read_class_time_table")
def read_class_time_table(request: RClassTimeTable, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 3:
        return {"status": 0, "message": "You are not authorized to view class time table entries!"}

    if request.id:
        entry = db.query(ClassTimeTable).filter(ClassTimeTable.id == request.id, ClassTimeTable.status == 1).first()
        if not entry:
            return {"status": 0, "message": "Class time table entry not found!"}
        return {"status": 1, "data": jsonable_encoder(entry)}

    all_entries = db.query(ClassTimeTable).filter(ClassTimeTable.status == 1).all()
    return {"status": 1, "data": jsonable_encoder(all_entries)}


# UPDATE CLASS TIME TABLE
@router.post("/update_class_time_table")
def update_class_time_table(request: UClassTimeTable, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can update class time table entries!"}

    entry = db.query(ClassTimeTable).filter(ClassTimeTable.id == request.id, ClassTimeTable.status == 1).first()
    if not entry:
        return {"status": 0, "message": "Class time table entry not found!"}

    entry.time_table_id = request.time_table_id
    entry.class_subject_id = request.class_subject_id
    entry.modified_by = requester.id

    db.commit()
    db.refresh(entry)

    return {"status": 1, "message": "Class time table entry updated successfully!"}


# DELETE CLASS TIME TABLE
@router.post("/drop_class_time_table")
def drop_class_time_table(request: DClassTimeTable, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can delete class time table entries!"}

    entry = db.query(ClassTimeTable).filter(ClassTimeTable.id == request.id, ClassTimeTable.status == 1).first()
    if not entry:
        return {"status": 0, "message": "Class time table entry not found or already deleted!"}

    entry.status = -1
    entry.modified_by = requester.id

    db.commit()
    db.refresh(entry)

    return {"status": 1, "message": "Class time table entry deleted successfully!"}
