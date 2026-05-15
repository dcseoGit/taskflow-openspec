import re
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from .. import models
from ..auth import create_token, get_current_user
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class SignupRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not EMAIL_RE.match(v):
            raise ValueError("올바른 이메일 형식이 아닙니다")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("비밀번호는 8자 이상이어야 합니다")
        return v


class LoginRequest(BaseModel):
    email: str
    password: str


def user_response(user: models.User, token: str) -> dict:
    return {"token": token, "user": {"id": user.id, "email": user.email, "team_id": user.team_id}}


@router.post("/signup", status_code=201)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == req.email).first():
        raise HTTPException(409, detail={"code": "EMAIL_TAKEN", "message": "이미 가입된 이메일입니다"})
    pw_hash = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode()
    user = models.User(email=req.email, password_hash=pw_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_response(user, create_token(user.id))


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email.lower()).first()
    if not user or not bcrypt.checkpw(req.password.encode(), user.password_hash.encode()):
        raise HTTPException(401, detail={"code": "INVALID_CREDENTIALS", "message": "이메일 또는 비밀번호가 일치하지 않습니다"})
    return user_response(user, create_token(user.id))


@router.post("/logout")
def logout():
    return {}


@router.get("/me")
def me(current_user: models.User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "team_id": current_user.team_id}
