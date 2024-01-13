from pydantic import BaseModel

class UserRequest(BaseModel):
    """
    User Request
    """    
    user_name: str
    
class UserTaskRequest(UserRequest):
    """
    User Task Request
    """
    user_name: str
    task_title: str
