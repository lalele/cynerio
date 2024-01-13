from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from task_manager.dependencies import get_db
from task_manager.schemas.user_task_request import UserRequest, UserTaskRequest
from task_manager.services.task_service import TaskService
from task_manager.services.user_service import UserService


router = APIRouter(prefix="/task", tags=["tasks"])


@router.post("/checkin", status_code=HTTP_201_CREATED)
def task_checkin(user_task_request: UserTaskRequest, db: Session = Depends(get_db)):
    """
    Check-in a new task and update the start time.

    Returns:
    None: This endpoint does not return any content.

    Raises:
    HTTPException(400): If the user has another open task.

    Example Request:
    POST /checkin
    {
        "user_name": "Bob",
        "task_title": "Complete Project A",
    }
    """
    try:
        user_service = UserService(db)
        db_user = user_service.get_user(user_task_request.user_name)

        if not db_user:
            db_user = user_service.create_user(user_name=user_task_request.user_name)

        task_service = TaskService(db)
        task_service.init_task(db_user.id, user_task_request.task_title, db_user.is_open_task)
        user_service.set_user_is_open_task(db_user, True)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


@router.put("/checkout")
def task_checkout(user_request: UserRequest, db: Session = Depends(get_db)):
    """
    Update task status to complete and record the end time.

    Returns:
    None: This endpoint does not return any content.

    Raises:
    HTTPException(404): If the specified user is not found.
    HTTPException(400): If the task is already checked-out.

    Example Request:
    PUT /checkout
    {
        "user_name": "Bob",
    }
    """

    try:
        user_service = UserService(db)
        db_user = user_service.get_user(user_request.user_name)

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
    
        TaskService(db).checkout_task(db_user.id, db_user.is_open_task)
        user_service.set_user_is_open_task(db_user, False)

        db.commit()
    except Exception as e:
        db.rollback()
        raise e