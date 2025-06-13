from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import text
from sqlalchemy import ForeignKey       
from app.models import Base


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:484848@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()   

#connection to alchemy database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()