from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

# issue fix - for building the db with alembic
try:
    from task_manager.db.database import Base
except ImportError:
    from db.database import Base


class TaskTimeFrame(Base):
    __tablename__ = "task_timeframes"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    task_id = Column(Integer, ForeignKey("tasks.id"), index=True, nullable=False)
    task = relationship("task.Task", back_populates="task_timeframes")
