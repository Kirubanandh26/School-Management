from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


db_url = "mysql+pymysql://root:Kerupa%4020eea14@localhost:3306/school_system_management"

engine = create_engine(db_url)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

