from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from task_manager.dependencies import get_db
from task_manager.schemas.user_task_response import TaskDurationResponse
from task_manager.services.task_service import TaskService

router = APIRouter(prefix="/report", tags=["reports"])


@router.get("/tasks_duration", response_model=list[TaskDurationResponse])
def get_tasks_duration(db: Session = Depends(get_db)):
    """
    Retrieve a list of tasks along with associated user name and their respective durations.

    Returns:
    List[TaskDurationResponse]: A list of task durations of users, each represented by a TaskDurationResponse object.

    Example Response:
    [
        {
            "user_name": "Bob",
            "task_title": "Complete Project A",
            "duration": 120,  # Duration in seconds
        },
        {
            "user_name": "Alice",
            "task_title": "Review Project B",
            "duration": 90,
        },
        # ... additional task durations
    ]
    """
    return TaskService(db).get_all_tasks_durations()
