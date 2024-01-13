from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from task_manager.api.task_check_api import router as task_check_router
from task_manager.api.report_tasks_api import router as report_tasks_router

app = FastAPI()

app.include_router(prefix="/api", router=task_check_router)
app.include_router(prefix="/api", router=report_tasks_router)

ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)