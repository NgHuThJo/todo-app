from typing import Annotated

from fastapi import APIRouter, Body
from pydantic import BaseModel

from models.db import DbSession
from models.task import Task

tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Create task
class CreateTaskRequest(BaseModel):
    is_checked: bool
    task: str

class CreateTaskResponse(BaseModel):
    id: int
    is_checked: bool
    task: str

@tasks_router.post("/", response_model=CreateTaskResponse)
async def create_task(body: Annotated[CreateTaskRequest, Body()], db: DbSession):
    task = Task(**body.model_dump())
    db.add(task)
    await db.commit()
    # Necessary if you need to populate entity with database-generated fields
    # Alternatively just query the entity again
    await db.refresh(task)

    return task


