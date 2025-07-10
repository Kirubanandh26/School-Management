from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# CREATE
@router.post("/create_exam_standard")
def create_exam_standard(request: CExamStandard, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can create exam standard entries!"}

    exists = db.query(ExamStandard).filter(
        ExamStandard.exam_id == request.exam_id,
        ExamStandard.standard_id == request.standard_id,
        ExamStandard.status == 1
    ).first()

    if exists:
        return {"status": 0, "message": "ExamStandard already exists!"}

    new_entry = ExamStandard(
        exam_id=request.exam_id,
        standard_id=request.standard_id,
        created_by=requester.id
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {"status": 1, "message": "ExamStandard created successfully!"}

# READ
@router.post("/read_exam_standard")
def read_exam_standard(request: RExamStandard, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation > 3:
        return {"status": 0, "message": "You are not authorized to view exam standards!"}

    if request.id:
        record = db.query(ExamStandard).filter(ExamStandard.id == request.id, ExamStandard.status == 1).first()
        if not record:
            return {"status": 0, "message": "ExamStandard not found!"}
        return {"status": 1, "data": jsonable_encoder(record)}

    records = db.query(ExamStandard).filter(ExamStandard.status == 1).all()
    return {"status": 1, "data": jsonable_encoder(records)}

# UPDATE
@router.post("/update_exam_standard")
def update_exam_standard(request: UExamStandard, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can update exam standard entries!"}

    record = db.query(ExamStandard).filter(ExamStandard.id == request.id, ExamStandard.status == 1).first()
    if not record:
        return {"status": 0, "message": "ExamStandard not found!"}

    record.exam_id = request.exam_id
    record.standard_id = request.standard_id
    record.modified_by = requester.id

    db.commit()
    db.refresh(record)

    return {"status": 1, "message": "ExamStandard updated successfully!"}

# DELETE
@router.post("/drop_exam_standard")
def drop_exam_standard(request: DExamStandard, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 1:
        return {"status": 0, "message": "Only admin can delete exam standard entries!"}

    record = db.query(ExamStandard).filter(ExamStandard.id == request.id, ExamStandard.status == 1).first()
    if not record:
        return {"status": 0, "message": "ExamStandard not found or already deleted!"}

    record.status = -1
    record.modified_by = requester.id

    db.commit()
    db.refresh(record)

    return {"status": 1, "message": "ExamStandard deleted successfully!"}
