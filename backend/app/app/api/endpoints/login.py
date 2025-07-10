from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from db.session import get_db
from schemas import *
from sqlalchemy import or_
from models import *
from ..deps import token_generation

router = APIRouter()

@router.post("/login")
def login(request: Login, db: Session = Depends(get_db)):

    db.query(Token).filter(Token.reg_no==request.reg_no).update({Token.status:-1})
    db.commit()
    return token_generation(request, db)



    




   