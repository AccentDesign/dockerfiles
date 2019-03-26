from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from typing import List, Optional

from app.auth.models import User
from app.middleware import DatabaseMiddleware


def get_db(request: Request):
    return request.state.db


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]


class UserIn(UserBase):
    password: Optional[str]


class UserOut(UserBase):
    id: int


def add_user(db_session: Session, user_in: UserIn):
    user = User(**user_in.dict())
    if user_in.password:
        user.set_password(user_in.password)
    return user.save(db_session)


app = FastAPI()
app.add_middleware(DatabaseMiddleware)


@app.get("/users/", response_model=List[UserOut])
async def list_users(db: Session = Depends(get_db)):
    users = db.query(User)
    return [user for user in users]


@app.post("/users/", response_model=UserOut)
async def create_user(*, user_in: UserIn, db: Session = Depends(get_db)):
    try:
        return add_user(db, user_in=user_in)
    except IntegrityError as e:
        msg = e.args[0]
        detail = [{"loc": ["database"], "msg": msg, "type": "integrity"}]
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user
