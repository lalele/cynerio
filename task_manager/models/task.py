from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# issue fix - for building the db with alembic
try:
    from task_manager.db.database import Base
except ImportError:
    from db.database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("user.User", back_populates="tasks")
    task_timeframes = relationship("TaskTimeFrame", back_populates="task")
    duration = Column(Integer, default=0)

from .task_timeframe import TaskTimeFrame