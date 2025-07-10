from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token
from sqlalchemy import and_, func, desc
from datetime import date

router = APIRouter()

def calculate_percentage(marks):
    return round(sum(marks) / len(marks), 2) if marks else 0.0

def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "F"

# CREATE MARK
@router.post("/create_mark")
def create_mark(request: CMark, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation != 3:
        return {"status": 0, "message": "Only class teachers can create marks!"}

    academic_data = db.query(AcademicData).filter(AcademicData.id == request.academic_data_id, AcademicData.status == 1).first()
    if not academic_data:
        return {"status": 0, "message": "Academic data not found!"}

    target_user = db.query(User).filter(User.id == academic_data.user_id, User.status == 1).first()
    dynamic_data = db.query(DynamicData).filter(DynamicData.user_id == target_user.id).first()

    if requester.tutor_class_id != dynamic_data.class_room_id:
        return {"status": 0, "message": "You can only assign marks to students in your class!"}

    exists = db.query(Mark).filter(
        Mark.academic_data_id == request.academic_data_id,
        Mark.exam_standard_id == request.exam_standard_id,
        Mark.status == 1
    ).first()
    if exists:
        return {"status": 0, "message": "Mark already exists for this exam and student!"}

    grade = get_grade(request.mark)

    new_mark = Mark(
        mark=request.mark,
        grade=grade,
        exam_standard_id=request.exam_standard_id,
        academic_data_id=request.academic_data_id,
        created_by=requester.id
    )
    db.add(new_mark)
    db.commit()
    db.refresh(new_mark)

    return {"status": 1, "message": "Mark added successfully!"}


# READ MARK
@router.post("/read_mark")
def read_mark(request: RMark, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if request.reg_no:
        target_user = db.query(User).filter(User.reg_no == request.reg_no, User.status == 1).first()
    else:
        target_user = requester

    if not target_user:
        return {"status": 0, "message": "Target user not found!"}

    academic = db.query(AcademicData).filter(AcademicData.user_id == target_user.id, AcademicData.status == 1).first()
    if not academic:
        return {"status": 0, "message": "Academic data not found!"}

    dynamic = db.query(DynamicData).filter(DynamicData.user_id == target_user.id).first()

    if requester.designation == 4 and requester.id != target_user.id:
        return {"status": 0, "message": "Students can only view their own marks!"}

    if requester.designation == 3 and requester.tutor_class_id != dynamic.class_room_id:
        return {"status": 0, "message": "You can only view marks for your class!"}

    if requester.designation == 2 and target_user.designation != 3:
        return {"status": 0, "message": "Principal can view marks of teachers only!"}

    marks = db.query(Mark).filter(Mark.academic_data_id == academic.id, Mark.status == 1).all()
    if not marks:
        return {"status": 0, "message": "No marks found!"}

    percentage = calculate_percentage([m.mark for m in marks])
    grade = get_grade(percentage)

    all_academic_ids = db.query(DynamicData.id).filter(DynamicData.class_room_id == dynamic.class_room_id).subquery()
    class_academic_ids = db.query(AcademicData.id).filter(AcademicData.dynamic_data_id.in_(all_academic_ids)).subquery()

    all_students = db.query(
        Mark.academic_data_id,
        func.avg(Mark.mark).label("avg")
    ).filter(Mark.academic_data_id.in_(class_academic_ids)).group_by(Mark.academic_data_id).order_by(desc("avg")).all()

    rank = next((i+1 for i, m in enumerate(all_students) if m.academic_data_id == academic.id), None)

    result = [{"exam_standard_id": m.exam_standard_id, "mark": m.mark, "grade": m.grade} for m in marks]

    return {
        "status": 1,
        "data": result,
        "percentage": percentage,
        "grade": grade,
        "rank": rank
    }


@router.post("/mark_stats")
def mark_stats(request: TokenBase, db: Session = Depends(get_db)):
    requester_reg = verify_token(request.token, db)
    requester = db.query(User).filter(User.reg_no == requester_reg).first()

    if requester.designation == 3:
        students = db.query(DynamicData.id).filter(DynamicData.class_room_id == requester.tutor_class_id).subquery()
        academic_ids = db.query(AcademicData.id).filter(AcademicData.dynamic_data_id.in_(students)).subquery()
    elif requester.designation == 2:
        teacher_ids = db.query(User.id).filter(User.designation == 3).subquery()
        academic_ids = db.query(AcademicData.id).filter(AcademicData.user_id.in_(teacher_ids)).subquery()
    elif requester.designation == 1:
        academic_ids = db.query(AcademicData.id).subquery()
    else:
        return {"status": 0, "message": "Not authorized to view statistics!"}

    marks = db.query(Mark).filter(Mark.academic_data_id.in_(academic_ids), Mark.status == 1).all()
    if not marks:
        return {"status": 0, "message": "No marks data found!"}

    total_students = len(set(m.academic_data_id for m in marks))
    pass_count = len([m for m in marks if m.mark >= 50])

    average = calculate_percentage([m.mark for m in marks])
    pass_percent = round((pass_count / len(marks)) * 100, 2) if marks else 0.0

    return {
        "status": 1,
        "data": {
            "pass_percentage": pass_percent,
            "average_percentage": average,
            "total_students": total_students
        }
    }
