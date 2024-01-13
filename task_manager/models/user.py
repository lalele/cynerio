from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

# issue fix - for building the db with alembic
try:
    from task_manager.db.database import Base
except ImportError:
    from db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    is_open_task = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="user")

from .task import Task
