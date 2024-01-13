from task_manager.models.user import User
from task_manager.services.base_service import BaseService


class UserService(BaseService):
    """
    User Service
    """
    def get_user(self, user_name: str):
        """
        Get a user
        """
        return self.db.query(User).filter(User.name == user_name).first()
    
    def create_user(self, user_name: str) -> User:
        """
        Create a new user
        """
        db_user = User(name=user_name, is_open_task=False)
        self.db.add(db_user)
        self.db.flush()
        return db_user
    
    def set_user_is_open_task(self, user: User, is_open_task: bool):
        """
        Set user's is_open_task to True
        """
        user.is_open_task = is_open_task
    