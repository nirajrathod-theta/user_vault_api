from fastapi import Depends, FastAPI
from database.database import Base, engine, get_db
from database.db_schemas import *
from auth.auth import auth_router
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test(db: Session = Depends(get_db)):

    users = db.query(DBUser).all()

    return users

# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}