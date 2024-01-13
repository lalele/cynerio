from fastapi.testclient import TestClient
from task_manager.db.database import Base, SessionLocal, engine
from task_manager.main import app


client = TestClient(app)

class TestTaskCheckAPI:           
    def test_task_checkin(self):
        """
        Test a succssful task check-in
        """
        # check-in
        payload = {"user_name": "Roy", "task_title": "Buy a new car"}
        response = client.post("/api/task/checkin", json=payload)

        assert response.status_code == 201
        assert response.json() is None


    def test_only_one_task_checked_in(self):
        """
        Test a failed task check-in due to multiple check-ins
        """
        # check-in twice
        payload = {"user_name": "Bobik", "task_title": "Buy a new car"}

        response = client.post("/api/task/checkin", json=payload)
        response = client.post("/api/task/checkin", json=payload)
        assert response.status_code == 400

        # with a different task
        payload = {"user_name": "Bobik", "task_title": "Sell the old car"}
        response = client.post("/api/task/checkin", json=payload)
        assert response.status_code == 400

    def test_task_checkout(self):
        """
        Test a succssful task check-out
        """
        # complete a task
        payload = {"user_name": "Tom", "task_title": "Buy a new car"}
        response = client.post("/api/task/checkin", json=payload)
        assert response.status_code == 201
        assert response.json() is None
        payload = {"user_name": "Tom"}
        response = client.put("/api/task/checkout", json=payload)
        assert response.status_code == 200
        assert response.json() is None

    def test_no_task_to_checkout(self):
        """
        Test a failed task check-out while task doesn't exist
        """
        # complete a task
        payload = {"user_name": "Rotem", "task_title": "Buy a new car"}
        response = client.post("/api/task/checkin", json=payload)
        assert response.status_code == 201
        assert response.json() is None
        payload = {"user_name": "Rotem"}
        response = client.put("/api/task/checkout", json=payload)
        assert response.status_code == 200
        assert response.json() is None

        # try to re-complete the task
        payload = {"user_name": "Rotem"}
        response = client.put("/api/task/checkout", json=payload)
        assert response.status_code == 400

    def test_no_user_to_checkout(self):
        """
        Test a failed task check-out while task doesn't exist
        """
        # checkout with an unregistered user
        payload = {"user_name": "Jery"}
        response = client.put("/api/task/checkout", json=payload)
        assert response.status_code == 404