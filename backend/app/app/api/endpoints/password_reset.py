from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import *
from models import *
from db.session import get_db
from core.hashing import hash_password
from utils import send_email  
import random

router = APIRouter()


@router.post("/request-otp")
def request_password_reset(data: RequestOtp, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.mail == data.mail).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")

    otp = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=10)

    db_otp = PasswordReset(mail=data.mail, otp=otp, expires_at=expiry)
    db.add(db_otp)
    db.commit()

    send_email(to=data.mail, subject="Password Reset OTP", body=f"Your OTP is: {otp}")

    return {"msg": "OTP sent to your email"}




@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    otp_entry = db.query(PasswordReset).filter(
        PasswordReset.email == data.email,
        PasswordReset.otp == data.otp
    ).order_by(PasswordReset.expires_at.desc()).first()

    if not otp_entry or otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(User).filter(User.email == data.email).first()
    user.password = hash_password(data.new_password)
    db.commit()

    return {"msg": "Password reset successfully"}
