from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from .. import models
from ..auth import get_current_user
from ..database import get_db
from .teams import require_member

router = APIRouter(tags=["tasks"])

VALID_STATUSES = {"TODO", "DOING", "DONE"}


def task_response(task: models.Task) -> dict:
    return {
        "id": task.id, "team_id": task.team_id, "title": task.title, "status": task.status,
        "creator": {"id": task.creator.id, "email": task.creator.email},
        "assignee": {"id": task.assignee.id, "email": task.assignee.email} if task.assignee else None,
        "created_at": task.created_at,
    }


class CreateTaskRequest(BaseModel):
    title: str
    assignee_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not 1 <= len(v) <= 100:
            raise ValueError("제목은 100자 이내여야 합니다")
        return v


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    assignee_id: Optional[int] = None


class UpdateStatusRequest(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in VALID_STATUSES:
            raise ValueError("올바른 상태값이 아닙니다")
        return v


@router.get("/teams/{team_id}/tasks")
def get_tasks(
    team_id: int,
    filter: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    require_member(team_id, current_user, db)
    q = db.query(models.Task).filter(models.Task.team_id == team_id)
    if filter == "me":
        q = q.filter(models.Task.assignee_id == current_user.id)
    elif filter == "unassigned":
        q = q.filter(models.Task.assignee_id.is_(None))
    tasks = q.order_by(models.Task.created_at.desc()).all()
    return [task_response(t) for t in tasks]


@router.post("/teams/{team_id}/tasks", status_code=201)
def create_task(
    team_id: int,
    req: CreateTaskRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    require_member(team_id, current_user, db)
    task = models.Task(team_id=team_id, title=req.title, creator_id=current_user.id, assignee_id=req.assignee_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task_response(task)


@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "해당 항목을 찾을 수 없습니다"})
    require_member(task.team_id, current_user, db)
    return task_response(task)


@router.put("/tasks/{task_id}")
def update_task(task_id: int, req: UpdateTaskRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "해당 항목을 찾을 수 없습니다"})
    require_member(task.team_id, current_user, db)
    if req.title is not None:
        task.title = req.title.strip()
    if "assignee_id" in req.model_fields_set:
        task.assignee_id = req.assignee_id
    db.commit()
    db.refresh(task)
    return task_response(task)


@router.patch("/tasks/{task_id}/status")
def update_task_status(task_id: int, req: UpdateStatusRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "해당 항목을 찾을 수 없습니다"})
    require_member(task.team_id, current_user, db)
    task.status = req.status
    db.commit()
    db.refresh(task)
    return task_response(task)


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "해당 항목을 찾을 수 없습니다"})
    team = require_member(task.team_id, current_user, db)
    if task.creator_id != current_user.id and team.owner_id != current_user.id:
        raise HTTPException(403, detail={"code": "FORBIDDEN", "message": "권한이 없습니다"})
    db.delete(task)
    db.commit()
