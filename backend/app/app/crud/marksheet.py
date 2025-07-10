from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import func
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os
from app.models.mark import Mark
from app.models.user import User
from app.models.subject import Subject
from app.models.exam import Exam
from app.models.classes import Classes


def display(student_id:int,db:Session):
    query = (
        db.query(Mark, User, Subject, Exam, Classes)
        .outerjoin(Subject, Subject.id == Mark.subject_id)
        .outerjoin(Exam, Exam.id == Mark.exam_id)
        .join(User, User.id == Mark.student_id)
        .join(Classes, Classes.id == User.classes_id)
        .filter(User.id == student_id)
        .all()
    )

    if not query:
        raise HTTPException(status_code=404, detail="No data found")

    student = query[0][1]
    classes = query[0][4]

    exam_subjects = {}
    for mark, user, subject, exam, cls in query:
        if exam.name not in exam_subjects:
            exam_subjects[exam.name] = {}
        if mark and mark.mark is not None:
            exam_subjects[exam.name][subject.name] = {"mark": mark.mark, "grade": mark.grade}
        else:
            exam_subjects[exam.name][subject.name] = {"mark": "AB", "grade": "NA"}

    exam_ranks = {}
    for exam_name in exam_subjects.keys():
        exam_obj = db.query(Exam).filter(Exam.name == exam_name).first()
        if exam_obj:
            totals = (
                db.query(Mark.student_id, func.sum(Mark.mark).label("total"))
                .filter(Mark.exam_id == exam_obj.id)
                .group_by(Mark.student_id)
                .order_by(func.sum(Mark.mark).desc())
                .all()
            )
            rank = 1
            for sid, _ in totals:
                if sid == student.id:
                    exam_ranks[exam_name] = rank
                    break
                rank += 1

    pdf_filename = f"marksheet_of_{student.name}.pdf"
    pdf_path = os.path.join("generated_pdfs", pdf_filename)
    os.makedirs("generated_pdfs", exist_ok=True)
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y, "AAA SCHOOL")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Name: {student.name}    Roll No: {student.roll_no}    Class ID: {classes.id}")
    y -= 30

    for exam_name, subjects in exam_subjects.items():
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"Exam: {exam_name}    Rank: {exam_ranks.get(exam_name, 'NA')}")
        y -= 20

        data = [["Subject", "Mark", "Grade"]]
        total = 0
        count = 0

        for subject, mark_info in subjects.items():
            mark = mark_info["mark"]
            grade = mark_info["grade"]
            data.append([subject, mark, grade])
            if isinstance(mark, (int, float)):
                total += mark
                count += 1

        data.append(["", "", ""])
        data.append(["Total", f"{total} / {count * 100 if count else 0}", ""])

        table = Table(data, colWidths=[200, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ]))

        table_height = 20 * len(data)
        table.wrapOn(c, width, height)
        table.drawOn(c, 50, y - table_height)
        y -= table_height + 40

        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    return (FileResponse(path=pdf_path, filename=pdf_filename, media_type="application/pdf")
)