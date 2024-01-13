import pytest
from task_manager.db.database import Base, SessionLocal, engine

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()
