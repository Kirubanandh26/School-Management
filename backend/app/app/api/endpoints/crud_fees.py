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

@router.post("/create_fees")
def create_fees(request: CFees, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 2:
        return {"status": 0, "message": "Only admin and principal can create fees!"}

    new_fees = Fees(
        academic_id=request.academic_id,
        tearm_id=request.tearm_id,
        total_fees=request.total_fees,
        paid_fees=request.paid_fees,
        due_date=request.due_date,
        late_charges=request.late_charges,
        created_by=requester.id
    )

    db.add(new_fees)
    db.commit()
    db.refresh(new_fees)

    return {"status": 1, "message": "Fees record created successfully!"}


@router.post("/read_fees")
def read_fees(request: RFees, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 2:
        return {"status": 0, "message": "Only admin and principal can view fees records!"}

    if request.id:
        fees = db.query(Fees).filter(Fees.id == request.id, Fees.status == 1).first()
        if not fees:
            return {"status": 0, "message": "Fees record not found!"}
        return {"status": 1, "data": {
            "id": fees.id,
            "academic_id": fees.academic_id,
            "tearm_id": fees.tearm_id,
            "total_fees": fees.total_fees,
            "paid_fees": fees.paid_fees,
            "due_date": fees.due_date.strftime("%Y-%m-%d"),
            "late_charges": fees.late_charges
        }}

    all_fees = db.query(Fees).filter(Fees.status == 1).all()
    readable = [{
        "id": f.id,
        "academic_id": f.academic_id,
        "tearm_id": f.tearm_id,
        "total_fees": f.total_fees,
        "paid_fees": f.paid_fees,
        "due_date": f.due_date.strftime("%Y-%m-%d"),
        "late_charges": f.late_charges
    } for f in all_fees]

    return {"status": 1, "data": readable}


@router.post("/update_fees")
def update_fees(request: UFees, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 2:
        return {"status": 0, "message": "Only admin and principal can update fees!"}

    fees = db.query(Fees).filter(Fees.id == request.id, Fees.status == 1).first()
    if not fees:
        return {"status": 0, "message": "Fees record not found!"}

    if request.academic_id is not None:
        fees.academic_id = request.academic_id
    if request.tearm_id is not None:
        fees.tearm_id = request.tearm_id
    if request.total_fees is not None:
        fees.total_fees = request.total_fees
    if request.paid_fees is not None:
        fees.paid_fees = request.paid_fees
    if request.due_date is not None:
        fees.due_date = request.due_date
    if request.late_charges is not None:
        fees.late_charges = request.late_charges

    fees.modified_by = requester.id
    db.commit()
    db.refresh(fees)

    return {"status": 1, "message": "Fees updated successfully!"}


@router.post("/drop_fees")
def drop_fees(request: RFees, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 2:
        return {"status": 0, "message": "Only admin and principal can delete fees!"}

    fees = db.query(Fees).filter(Fees.id == request.id, Fees.status == 1).first()
    if not fees:
        return {"status": 0, "message": "Fees record not found!"}

    fees.status = 0
    fees.modified_by = requester.id
    db.commit()

    return {"status": 1, "message": "Fees record deleted successfully!"}
