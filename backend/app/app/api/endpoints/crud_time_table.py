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
@router.post("/create_timetable")
def create_timetable(request: CTimeTable, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can create timetable entries!"}

    target = db.query(TimeTable).filter(
        TimeTable.day == request.day,
        TimeTable.period_no == request.period_no
    ).first()

    if target:
        if target.status == 1:
            return {"status": 0, "message": "Timetable entry already exists for this day and period!"}
        else:
            target.status = 1
            target.modified_by = requester.id
            db.commit()
            db.refresh(target)
            return {"status": 1, "message": "Timetable entry reactivated successfully!"}

    new_timetable = TimeTable(
        day=request.day,
        period_no=request.period_no,
        created_by=requester.id
    )

    db.add(new_timetable)
    db.commit()
    db.refresh(new_timetable)

    return {"status": 1, "message": "Timetable entry created successfully!"}




#READ
@router.post("/read_timetable")
def read_timetable(request: RTimeTable, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 3:
        return {"status": 0, "message": "You're not authorized to view timetable entries!"}

    if request.id:
        target = db.query(TimeTable).filter(TimeTable.id == request.id, TimeTable.status == 1).first()
        if not target:
            return {"status": 0, "message": "Timetable entry not found!"}
        return {"status": 1, "data": {"id": target.id, "day": target.day, "period_no": target.period_no}}

    all_entries = db.query(TimeTable).filter(TimeTable.status == 1).all()
    return {
        "status": 1,
        "data": [{"id": t.id, "day": t.day, "period_no": t.period_no} for t in all_entries]
    }



# UPDATE
@router.post("/update_timetable")
def update_timetable(request: UTimeTable, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can update timetable entries!"}

    timetable = db.query(TimeTable).filter(TimeTable.id == request.id, TimeTable.status == 1).first()
    if not timetable:
        return {"status": 0, "message": "Timetable entry not found!"}

    timetable.day = request.update_day
    timetable.period_no = request.update_period_no
    timetable.modified_by = requester.id

    db.commit()
    db.refresh(timetable)

    return {"status": 1, "message": "Timetable updated successfully!"}



# DELETE
@router.post("/drop_timetable")
def drop_timetable(request: DTimeTable, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can delete timetable entries!"}

    timetable = db.query(TimeTable).filter(TimeTable.id == request.id, TimeTable.status == 1).first()
    if not timetable:
        return {"status": 0, "message": "Timetable entry not found or already deleted!"}

    timetable.status = -1
    timetable.modified_by = requester.id

    db.commit()
    db.refresh(timetable)

    return {"status": 1, "message": "Timetable deleted successfully!"}
