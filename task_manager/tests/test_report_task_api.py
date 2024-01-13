from fastapi.testclient import TestClient

from task_manager.main import app
from task_manager.tests.utils.test_utils import TestUtils

client = TestClient(app)

class TestReportTaskAPI:
   
    def test_get_tasks_duration(self, db_session):
        """
        Test get report of tasks of users and their durations
        """
        # TODO: after fixing the way test db works to rollback data, remove it
        TestUtils.remove_db_data(db_session)
        
        user_tasks = [
           {"user_name": "A", "task_title": "Task 1", "duration": 259200},
           {"user_name": "B", "task_title": "Task 2", "duration": 250000},
           {"user_name": "C", "task_title": "Task 3", "duration": 252000}
        ]

        for user_task in user_tasks:
            TestUtils.create_user_and_task(db_session, user_task["user_name"], user_task["task_title"], user_task["duration"])      

        response = client.get("/api/report/tasks_duration")

        assert response.status_code == 200
        task_durations = response.json()
        
        assert task_durations == user_tasks

