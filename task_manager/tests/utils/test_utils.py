from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from task_manager.models.task import Task
from task_manager.models.task_timeframe import TaskTimeFrame
from task_manager.models.user import User

class TestUtils:
    """
    Test utils 
    """
    @staticmethod
    def create_user_and_task(db: Session, user_name: str, task_title: str, duration: int):
        """
        Create a new user, task and timeframe of 3 seconds and add it to the database.
        """
        new_user = User(name=user_name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)        

        new_task = Task(title=task_title, user_id=new_user.id, duration=duration)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

    @staticmethod
    def remove_db_data(db: Session):
        """
        Remove DB data
        """
        TestUtils.remove_all_task_timeframes(db)
        TestUtils.remove_all_tasks(db)
        TestUtils.remove_all_users(db)
    
    @staticmethod
    def remove_all_tasks(db: Session):
        """
        Remove DB Task's data
        """
        db.query(Task).delete()
        db.commit()

    @staticmethod
    def remove_all_task_timeframes(db: Session):
        """
        Remove DB TaskTimeFrame's data
        """        
        db.query(TaskTimeFrame).delete()
        db.commit()

    @staticmethod
    def remove_all_users(db: Session):
        """
        Remove DB User's data
        """          
        db.query(User).delete()
        db.commit()
        