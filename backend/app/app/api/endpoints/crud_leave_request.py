from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token
from datetime import date

router = APIRouter()

valid_statuses = ["p", "ab", "h", "fhp", "shp"]

def is_direct_superior(superior: int, target: int):
    return (
        (target == 4 and superior == 3) or
        (target == 3 and superior == 2) or
        (target == 2 and superior == 1)
    )

# CREATE
@router.post("/create_leave_request")
def create_leave_request(request: CLeaveRequest, db: Session = Depends(get_db)):
    if request.attendance_status not in valid_statuses:
        return {"status": 0, "message": "Invalid attendance status!"}

    reg_no = verify_token(request.token, db)
    user = db.query(User).filter(User.reg_no == reg_no).first()

    academic = db.query(AcademicData).filter(AcademicData.id == request.academic_id, AcademicData.status == 1).first()
    if not academic:
        return {"status": 0, "message": "Academic data not found!"}

    leave = LeaveRequest(
        user_id=user.id,
        academic_id=request.academic_id,
        from_date=request.from_date,
        till_date=request.till_date,
        description=request.description,
        created_by=user.id,
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)

    return {"status": 1, "message": "Leave request submitted successfully!"}


# READ
@router.post("/read_leave_request")
def read_leave_request(request: RLeaveRequest, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if request.reg_no:
        target = db.query(User).filter(User.reg_no == request.reg_no, User.status == 1).first()
        if not target:
            return {"status": 0, "message": "Target user not found!"}

        if requester.id != target.id and not is_direct_superior(requester.designation, target.designation):
            return {"status": 0, "message": "Unauthorized to view this user's leave requests!"}

        academic_ids = db.query(AcademicData.id).filter(AcademicData.user_id == target.id).subquery()
        leaves = db.query(LeaveRequest).filter(LeaveRequest.academic_id.in_(academic_ids), LeaveRequest.status == 1).all()
    else:
        academic_ids = db.query(AcademicData.id).filter(AcademicData.user_id == requester.id).subquery()
        leaves = db.query(LeaveRequest).filter(LeaveRequest.academic_id.in_(academic_ids), LeaveRequest.status == 1).all()

    return {
        "status": 1,
        "data": [
            {
                "id": i.id,
                "from_date": i.from_date,
                "till_date": i.till_date,
                "description": i.description,
                "approved_by": i.approved_by
            }
            for i in leaves
        ]
    }


# UPDATE (Approval or Status Change)
@router.post("/update_leave_request")
def update_leave_request(request: ULeaveRequest, db: Session = Depends(get_db)):
    if request.attendance_status not in valid_statuses:
        return {"status": 0, "message": "Invalid attendance status!"}

    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == request.id, LeaveRequest.status == 1).first()
    if not leave:
        return {"status": 0, "message": "Leave request not found!"}

    target_user = db.query(User).filter(User.id == leave.user_id).first()
    if not is_direct_superior(requester.designation, target_user.designation):
        return {"status": 0, "message": "Only direct superior can update this leave request!"}

    leave.description = f"Marked as {request.attendance_status}"
    leave.approved_by = requester.id
    leave.modified_by = requester.id

    db.commit()
    db.refresh(leave)

    return {"status": 1, "message": "Leave request updated successfully!"}


# DELETE
@router.post("/drop_leave_request")
def drop_leave_request(request: DLeaveRequest, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == request.id, LeaveRequest.status == 1).first()
    if not leave:
        return {"status": 0, "message": "Leave request not found or already deleted!"}

    target = db.query(User).filter(User.id == leave.user_id).first()
    if not is_direct_superior(requester.designation, target.designation):
        return {"status": 0, "message": "Only direct superior can delete this leave request!"}

    leave.status = -1
    leave.modified_by = requester.id

    db.commit()
    return {"status": 1, "message": "Leave request deleted successfully!"}
