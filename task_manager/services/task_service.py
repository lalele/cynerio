from typing import Optional
from fastapi import HTTPException
from datetime import datetime

from sqlalchemy.orm import joinedload

from task_manager.models.task import Task
from task_manager.models.task_timeframe import TaskTimeFrame
from task_manager.schemas.user_task_response import TaskDurationResponse
from task_manager.services.base_service import BaseService


class TaskService(BaseService):
    """
    Task Service
    """
    def init_task(self, user_id: int, task_title: str, is_open_task: bool) -> None:
        """
        Initialize a new task - get task or create and set a start time
        """
        self._validate_user_allowed_open_task(is_open_task)
        task = self._get_task(user_id, task_title)
        if not task:
            task = self._create_task(user_id, task_title, is_open_task)
        self._create_task_timeframe(task.id)
    
    def checkout_task(self, user_id: int, is_open_task: bool) -> None:
        """
        Check out task
        """
        utc_now = datetime.utcnow()
        self._validate_task_is_opened(is_open_task)
        last_task = self._get_user_last_task(user_id)
        task_timeframe = self._get_task_timeframe(last_task.id)    
        self._validate_task_timeframe_not_closed(task_timeframe)
        self._set_task_end_time(task_timeframe, utc_now)
        self._update_task_duration(last_task, task_timeframe.start_time, utc_now)

    def get_all_tasks_durations(self):
        """
        Get all tasks with user names and theirs durations
        """
        tasks = self.db.query(Task).options(joinedload(Task.user)).all()

        return [TaskDurationResponse(user_name=task.user.name, task_title=task.title, duration=task.duration) for task in tasks]

    def _update_task_duration(self, task: Task, start_time: datetime, end_time: datetime) -> None:
        """
        Update task duration by adding the new task timeframe duration
        """
        time_delta = end_time - start_time
        task.duration += int(time_delta.total_seconds())

    def _get_user_last_task(self, user_id) -> Optional[Task]:
        """
        Get user last task
        """
        return self.db.query(Task).filter(Task.user_id == user_id).order_by(Task.id.desc()).first()
    
    def _get_task_timeframe(self, task_id: int) -> Optional[TaskTimeFrame]:
        """
        Get task timeframe by task_id
        """
        return (
                    self.db.query(TaskTimeFrame)
                    .filter(
                        TaskTimeFrame.task_id == task_id,
                    )
                    .order_by(TaskTimeFrame.id.desc())
                    .first()
                )
    
    @classmethod
    def _set_task_end_time(cls, task_timeframe: TaskTimeFrame, end_time: datetime) -> None:
        """
        Set task's end time
        """
        task_timeframe.end_time = end_time

    def _create_task(self, user_id: int, task_title: str, is_open_task: bool) -> Task:
        """
        Create a new task
        """                
        db_task = Task(title=task_title, user_id=user_id)
        self.db.add(db_task)
        self.db.flush()
        return db_task

    def _get_task(self, user_id: int, task_title: str) -> Optional[Task]:
        """
        Get task filtered by user name and task title
        """
        return self.db.query(Task).filter(
            Task.user_id == user_id, Task.title == task_title).first()


    @classmethod
    def _validate_task_timeframe_not_closed(cls, task_timeframe: TaskTimeFrame):
        """
        Validate task timeframe is not closed
        """
        if not task_timeframe or task_timeframe.end_time:
            raise HTTPException(status_code=400, detail="Task is closed")
        
    def _validate_task_belongs_user(self, user_id: int, task_title: str):
        """
        Validate that the task belongs to the user
        """
        task = self._get_task(user_id, task_title)
        if not task:
            raise HTTPException(status_code=403, detail="Not permitted")
    
    @classmethod
    def _validate_user_allowed_open_task(cls, is_open_task: bool):
        """
        Validate if user is allowed to open a new task
        """
        if is_open_task:
            raise HTTPException(status_code=400, detail="User already has an opened task")

    @classmethod
    def _validate_task_is_opened(cls, is_open_task):
        if not is_open_task:
            raise HTTPException(status_code=400, detail="Task wasn't opened")
      
    def _create_task_timeframe(self, task_id: int) -> None:
        """
        Create task timeframe with start_time of utc now
        """
        db_task_timeframe = TaskTimeFrame(start_time=datetime.utcnow(), task_id=task_id)
        self.db.add(db_task_timeframe)