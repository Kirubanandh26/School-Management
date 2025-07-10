from db.base import Base, engine
from models import *
from fastapi import FastAPI
from api.endpoints import api

Base.metadata.create_all(bind=engine) 

app = FastAPI(title="School System Management")

app.include_router(api.api_router)