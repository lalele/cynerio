from pydantic import BaseModel


class TaskDurationResponse(BaseModel):
    """
    Task Duration Response
    """
    user_name: str
    task_title: str
    duration: int