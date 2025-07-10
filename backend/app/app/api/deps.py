from sqlalchemy.orm import Session
from sqlalchemy import and_
import secrets
from fastapi import HTTPException, status, Depends
from db.session import get_db
from models import *
from core.hashing import verify_password
from schemas import *  


def token_generation(request: Login, db: Session):
    db_auth = db.query(User).filter(and_(User.reg_no == request.reg_no, User.status==1)).first()
    
    if not db_auth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid user!"
        )
    
    if not verify_password(request.password, db_auth.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password!"
        )
         
    token=secrets.token_urlsafe(40)
    db_token = Token(
        reg_no=request.reg_no,
        token=token
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return token



def verify_token(token:str,db:Session):
    
    token_check=db.query(Token).filter(and_(Token.token==token),Token.status==1).first()
    
    if not token_check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token !")
    
    else:
        return token_check.reg_no
    


#ROLES AND THIER AUTHORIZATIONS

roles = {
    1: "Admin",
    2: "Principal",
    3: "Teacher",
    4: "Student"
}

def is_allowed_to_manage(manager_role: int, target_role: int) :
    return manager_role < target_role