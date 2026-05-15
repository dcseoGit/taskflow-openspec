from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from .. import models
from ..auth import get_current_user
from ..database import get_db
from .teams import require_member

router = APIRouter(tags=["chat"])


class SendMessageRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("메시지를 입력하세요")
        if len(v) > 1000:
            raise ValueError(f"메시지는 1000자 이내로 입력하세요")
        return v


def message_response(msg: models.Message) -> dict:
    return {
        "id": msg.id, "team_id": msg.team_id,
        "user_id": msg.user_id, "user_email": msg.user.email,
        "content": msg.content, "created_at": msg.created_at,
    }


@router.get("/teams/{team_id}/messages")
def get_messages(
    team_id: int,
    since: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    require_member(team_id, current_user, db)
    q = db.query(models.Message).filter(models.Message.team_id == team_id)
    if since:
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            q = q.filter(models.Message.created_at > since_dt)
        except ValueError:
            raise HTTPException(400, detail={"code": "VALIDATION_ERROR", "message": "since 형식이 올바르지 않습니다"})
    else:
        q = q.order_by(models.Message.created_at.desc()).limit(50)
        messages = q.all()
        return [message_response(m) for m in reversed(messages)]
    messages = q.order_by(models.Message.created_at.asc()).all()
    return [message_response(m) for m in messages]


@router.post("/teams/{team_id}/messages", status_code=201)
def send_message(
    team_id: int,
    req: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    require_member(team_id, current_user, db)
    msg = models.Message(team_id=team_id, user_id=current_user.id, content=req.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return message_response(msg)


@router.delete("/messages/{message_id}", status_code=204)
def delete_message(message_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "해당 항목을 찾을 수 없습니다"})
    require_member(msg.team_id, current_user, db)
    if msg.user_id != current_user.id:
        raise HTTPException(403, detail={"code": "NOT_OWNER", "message": "본인의 메시지만 삭제할 수 있습니다"})
    db.delete(msg)
    db.commit()
