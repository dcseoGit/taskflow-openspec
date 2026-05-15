from datetime import datetime, timezone
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


def now_utc():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    team_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("teams.id", use_alter=True), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)

    team: Mapped["Team | None"] = relationship("Team", foreign_keys=[team_id], back_populates="members")
    owned_teams: Mapped[list["Team"]] = relationship("Team", foreign_keys="Team.owner_id", back_populates="owner")
    created_tasks: Mapped[list["Task"]] = relationship("Task", foreign_keys="Task.creator_id", back_populates="creator")
    assigned_tasks: Mapped[list["Task"]] = relationship("Task", foreign_keys="Task.assignee_id", back_populates="assignee")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user")


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    invite_code: Mapped[str] = mapped_column(String(9), unique=True, nullable=False, index=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)

    owner: Mapped["User"] = relationship("User", foreign_keys=[owner_id], back_populates="owned_teams")
    members: Mapped[list["User"]] = relationship("User", foreign_keys="User.team_id", back_populates="team")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="team", cascade="all, delete-orphan")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="team", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(Enum("TODO", "DOING", "DONE", name="task_status"), nullable=False, default="TODO")
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, index=True)

    team: Mapped["Team"] = relationship("Team", back_populates="tasks")
    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id], back_populates="created_tasks")
    assignee: Mapped["User | None"] = relationship("User", foreign_keys=[assignee_id], back_populates="assigned_tasks")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, index=True)

    team: Mapped["Team"] = relationship("Team", back_populates="messages")
    user: Mapped["User"] = relationship("User", back_populates="messages")
