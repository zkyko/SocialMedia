from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from . import models
from .database import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from . import schema
from .utils import hash  
from .routers import post, user, auth
from app import oauth2
from fastapi.middleware.cors import CORSMiddleware

##models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

while True:
    try:
        # THE ONLY CHANGE IS HERE: cursor_factory -> row_factory
        connection = psycopg.connect(
            host="localhost",
            port="5432",
            dbname="fastapi",
            user="postgres",
            password="484848",
            row_factory=dict_row  # Corrected parameter name for psycopg 3
        )
        cursor = connection.cursor()
        print("database connection was successful")
        break
    except Exception as e:
        print("Can't connect to the database")
        print(e)
        time.sleep(2)
    

@app.get("/")
def root():
    return {"message": "welcome to my social media api"}

    


