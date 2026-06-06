
from fastapi import FastAPI

from features.tasks import tasks_router

app = FastAPI()
app.include_router(tasks_router)
