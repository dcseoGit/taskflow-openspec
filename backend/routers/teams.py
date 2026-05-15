import random
import re
import string
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from .. import models
from ..auth import get_current_user
from ..database import get_db

router = APIRouter(prefix="/teams", tags=["teams"])

INVITE_CODE_RE = re.compile(r"^[A-Z]{4}-[0-9]{4}$")


def require_member(team_id: int, user: models.User, db: Session) -> models.Team:
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "해당 항목을 찾을 수 없습니다"})
    if user.team_id != team_id:
        raise HTTPException(403, detail={"code": "FORBIDDEN", "message": "권한이 없습니다"})
    return team


def generate_invite_code(db: Session) -> str:
    while True:
        letters = "".join(random.choices(string.ascii_uppercase, k=4))
        digits = "".join(random.choices(string.digits, k=4))
        code = f"{letters}-{digits}"
        if not db.query(models.Team).filter(models.Team.invite_code == code).first():
            return code


class CreateTeamRequest(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not 1 <= len(v) <= 30:
            raise ValueError("팀 이름은 30자 이내여야 합니다")
        return v


class JoinTeamRequest(BaseModel):
    invite_code: str

    @field_validator("invite_code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not INVITE_CODE_RE.match(v):
            raise ValueError("형식이 올바르지 않습니다")
        return v


@router.post("", status_code=201)
def create_team(req: CreateTeamRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    code = generate_invite_code(db)
    team = models.Team(name=req.name, invite_code=code, owner_id=current_user.id)
    db.add(team)
    db.flush()
    current_user.team_id = team.id
    db.commit()
    db.refresh(team)
    return {"id": team.id, "name": team.name, "invite_code": team.invite_code, "owner_id": team.owner_id, "created_at": team.created_at}


@router.post("/join")
def join_team(req: JoinTeamRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.team_id is not None:
        raise HTTPException(409, detail={"code": "ALREADY_IN_TEAM", "message": "이미 다른 팀에 소속되어 있습니다"})
    team = db.query(models.Team).filter(models.Team.invite_code == req.invite_code).first()
    if not team:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "해당 초대코드를 찾을 수 없습니다"})
    current_user.team_id = team.id
    db.commit()
    member_count = db.query(models.User).filter(models.User.team_id == team.id).count()
    return {"team": {"id": team.id, "name": team.name, "member_count": member_count}, "redirect": f"/teams/{team.id}"}


@router.get("/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    team = require_member(team_id, current_user, db)
    member_count = db.query(models.User).filter(models.User.team_id == team_id).count()
    return {"id": team.id, "name": team.name, "invite_code": team.invite_code, "owner_id": team.owner_id, "member_count": member_count, "created_at": team.created_at}


@router.get("/{team_id}/members")
def get_members(team_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    team = require_member(team_id, current_user, db)
    members = db.query(models.User).filter(models.User.team_id == team_id).order_by(models.User.created_at).all()
    return [
        {"id": m.id, "email": m.email, "role": "owner" if m.id == team.owner_id else "member", "joined_at": m.created_at}
        for m in members
    ]


@router.delete("/{team_id}/leave")
def leave_team(team_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    team = require_member(team_id, current_user, db)
    if team.owner_id == current_user.id:
        raise HTTPException(403, detail={"code": "OWNER_CANNOT_LEAVE", "message": "팀 소유자는 탈퇴할 수 없습니다"})
    current_user.team_id = None
    db.commit()
    return {}
