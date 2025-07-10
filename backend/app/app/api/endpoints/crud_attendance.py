# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from db.session import get_db
# from models import *
# from schemas import *
# from ..deps import verify_token
# from sqlalchemy import and_, func
# from datetime import date

# router = APIRouter()


# #CREATE
# @router.post("/create_attendance")
# def create_attendance(request: CAttendance, db: Session = Depends(get_db)):
#     requester_reg = verify_token(request.token, db)
#     requester = db.query(User).filter(User.reg_no == requester_reg).first()

#     target = db.query(User).filter(User.reg_no == request.reg_no, User.status == 1).first()
#     if not target:
#         return {"status": 0, "message": "Target user not found!"}

#     target_data = db.query(DynamicData).filter(DynamicData.user_id == target.id).first()
#     if not target_data:
#         return {"status": 0, "message": "No dynamic data for target!"}

#     academic_data = db.query(AcademicData).filter(
#         AcademicData.user_id == target.id,
#         AcademicData.status == 1
#     ).first()
#     if not academic_data:
#         return {"status": 0, "message": "Academic data not found!"}

#     # Permission Logic
#     if requester.designation == 1:
#         if target.designation != 2:
#             return {"status": 0, "message": "Admin can only mark attendance for Principal!"}
#     elif requester.designation == 2:
#         if target.designation != 3:
#             return {"status": 0, "message": "Principal can only mark attendance for Teachers!"}
#     elif requester.designation == 3:
#         if target.designation != 4:
#             return {"status": 0, "message": "Mentor can only mark attendance for students!"}
#         if not target_data.class_room_id:
#             return {"status": 0, "message": "Student is not assigned to a class!"}
#         if not requester.tutor_class_id or requester.tutor_class_id != target_data.class_room_id:
#             return {"status": 0, "message": "Mentor can only mark attendance for their own class students!"}
#     else:
#         return {"status": 0, "message": "Not authorized to mark attendance for this user!"}

#     exists = db.query(Attendance).filter(
#         Attendance.academic_id == academic_data.id,
#         Attendance.date == request.date,
#         Attendance.status == 1
#     ).first()
#     if exists:
#         return {"status": 0, "message": "Attendance already marked for this date!"}

#     new_attendance = Attendance(
#         academic_id=academic_data.id,
#         attendance_status=request.attendance_status,
#         date=request.date,
#         reg_no=request.reg_no,
#         created_by=requester.id
#     )
#     db.add(new_attendance)
#     db.commit()
#     db.refresh(new_attendance)

#     return {"status": 1, "message": "Attendance created successfully!"}


# #READ
# @router.post("/read_attendance")
# def read_attendance(request: RAttendance, db: Session = Depends(get_db)):
#     requester_reg = verify_token(request.token, db)
#     requester = db.query(User).filter(User.reg_no == requester_reg).first()

#     reg_no = request.reg_no or requester.reg_no

#     target = db.query(User).filter(User.reg_no == reg_no, User.status == 1).first()
#     if not target:
#         return {"status": 0, "message": "Target user not found!"}

#     dynamic = db.query(DynamicData).filter(DynamicData.user_id == target.id).first()
#     if not dynamic:
#         return {"status": 0, "message": "Dynamic data not found!"}

#     academic_data = db.query(AcademicData).filter(AcademicData.user_id == target.id, AcademicData.status == 1).first()
#     if not academic_data:
#         return {"status": 0, "message": "Academic data not found!"}

#     if requester.reg_no == reg_no:
#         pass 
#     elif requester.designation == 1 and target.designation == 2:
#         pass
#     elif requester.designation == 2 and target.designation == 3:
#         pass
#     elif requester.designation == 3 and target.designation == 4:
#         if not dynamic.class_room_id or dynamic.class_room_id != requester.tutor_class_id:
#             return {"status": 0, "message": "Teachers can only view attendance of their class students!"}
#     else:
#         return {"status": 0, "message": "Not authorized to view this attendance!"}

#     attendance_entries = db.query(Attendance).filter(
#         Attendance.academic_id == academic_data.id,
#         Attendance.status == 1
#     ).all()

#     total = len(attendance_entries)
#     present = len([a for a in attendance_entries if a.attendance_status == 1])
#     percentage = round((present / total) * 100, 2)

#     if requester.reg_no == reg_no:
#         return {"status": 1, "percentage": percentage}

#     attendance_data = [
#         {
#             "id": entry.id,
#             "date": entry.date.strftime("%Y-%m-%d"),
#             "status": "Present" if entry.attendance_status == 1 else "Absent"
#         }
#         for entry in attendance_entries
#     ]

#     return {
#         "status": 1,
#         "data": attendance_data,
#         "percentage": percentage
#     }

#     # If reg_no not given and requester is principal/admin, get teachers or principals
#     elif not request.reg_no and requester.designation in [1, 2]:
#         role_to_fetch = 2 if requester.designation == 1 else 3
#         targets = db.query(User).filter(User.designation == role_to_fetch, User.status == 1).all()
#         results = []

#         for user in targets:
#             academic = db.query(AcademicData).filter(
#                 AcademicData.user_id == user.id,
#                 AcademicData.status == 1
#             ).first()
#             if not academic:
#                 continue

#             attendance_entries = db.query(Attendance).filter(
#                 Attendance.academic_id == academic.id,
#                 Attendance.status == 1
#             ).all()
#             total = len(attendance_entries)
#             present = len([a for a in attendance_entries if a.attendance_status == 1])
#             percentage = attendance_percentage(total, present)

#             results.append({
#                 "reg_no": user.reg_no,
#                 "name": user.name,
#                 "total_days": total,
#                 "present_days": present,
#                 "percentage": percentage
#             })

#         return {"status": 1, "data": results}

#     # For individual read with reg_no
#     academic = db.query(AcademicData).filter(
#         AcademicData.user_id == target.id,
#         AcademicData.status == 1
#     ).first()
#     if not academic:
#         return {"status": 0, "message": "Academic data not found!"}

#     attendance_entries = db.query(Attendance).filter(
#         Attendance.academic_id == academic.id,
#         Attendance.status == 1
#     ).all()
#     total = len(attendance_entries)
#     present = len([a for a in attendance_entries if a.attendance_status == 1])
#     percentage = attendance_percentage(total, present)

#     data = [
#         {
#             "id": a.id,
#             "date": a.date.strftime("%Y-%m-%d"),
#             "status": "Present" if a.attendance_status == 1 else "Absent"
#         }
#         for a in attendance_entries
#     ]

#     return {"status": 1, "data": data, "percentage": percentage}


# #UPDATE
# @router.post("/update_attendance")
# def update_attendance(request: UAttendance, db: Session = Depends(get_db)):
#     requester_reg = verify_token(request.token, db)
#     requester = db.query(User).filter(User.reg_no == requester_reg).first()

#     attendance = db.query(Attendance).filter(Attendance.id == request.id, Attendance.status == 1).first()
#     if not attendance:
#         return {"status": 0, "message": "Attendance entry not found!"}

#     target = db.query(AcademicData).filter(AcademicData.id == attendance.academic_id).first()
#     target_user = db.query(User).filter(User.id == target.user_id).first()
#     dynamic_data = db.query(DynamicData).filter(DynamicData.user_id == target_user.id).first()

#     if requester.designation == 1:
#         pass
#     elif requester.designation == 2 and target_user.designation == 3:
#         pass
#     elif requester.designation == 3 and target_user.designation == 4:
#         if not dynamic_data or dynamic_data.class_room_id != requester.tutor_class_id:
#             return {"status": 0, "message": "Teacher can update attendance of their own class students only!"}
#     else:
#         return {"status": 0, "message": "Not authorized to update attendance for this user!"}

#     attendance.attendance_status = request.attendance_status
#     attendance.modified_by = requester.id

#     db.commit()
#     db.refresh(attendance)

#     return {"status": 1, "message": "Attendance updated successfully!"}
