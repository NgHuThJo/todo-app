from typing import Annotated

import structlog
from fastapi import APIRouter, Body, HTTPException, Path, Response
from pydantic import BaseModel, Field
from sqlalchemy import delete, select

from models.db import DbSession
from models.task import Task

tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger: structlog.stdlib.BoundLogger = structlog.get_logger()


# Create task
class CreateTaskRequest(BaseModel):
    is_checked: bool
    task: str = Field(min_length=1, max_length=255)


class CreateTaskResponse(BaseModel):
    id: int
    is_checked: bool
    task: str


@tasks_router.post("/", response_model=CreateTaskResponse)
async def create_task(body: Annotated[CreateTaskRequest, Body()], db: DbSession):
    statement = select(Task).where(Task.task == body.task)
    result = await db.execute(statement)
    duplicate_task = result.scalar()

    if duplicate_task is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Task with description '{body.task}' already exists",
        )

    task = Task(**body.model_dump())
    db.add(task)
    await db.commit()
    # Necessary if you need to populate entity with database-generated fields
    # Alternatively just query the entity again
    await db.refresh(task)

    return task


# Get all tasks
class GetAllTasksResponse(BaseModel):
    id: int
    is_checked: bool
    task: str


@tasks_router.get("/", response_model=list[GetAllTasksResponse])
async def get_all_tasks(db: DbSession):
    statement = select(Task)
    result = await db.execute(statement)
    tasks = result.scalars().all()

    return tasks


class UpdateTaskRequest(BaseModel):
    is_checked: bool
    task: str


@tasks_router.put("/{task_id}", status_code=204)
async def update_task(
    body: Annotated[UpdateTaskRequest, Body()],
    task_id: Annotated[int, Path()],
    db: DbSession,
):
    query_statement = select(Task).where(Task.id == task_id)
    result = await db.execute(query_statement)
    existing_task = result.scalars().first()

    if existing_task is None:
        raise HTTPException(
            status_code=422, detail=f"No task with id '{task_id}' found in database"
        )

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(existing_task, key, value)

    await db.commit()

    return Response(status_code=204)


@tasks_router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: Annotated[int, Path()], db: DbSession):
    query_statement = select(Task).where(Task.id == task_id)
    result = await db.execute(query_statement)
    existing_task = result.scalars().first()

    if existing_task is None:
        raise HTTPException(
            status_code=422,
            detail=f"Task with id '{task_id}' does not exist in database",
        )

    await db.delete(existing_task)

    await db.commit()

    return Response(status_code=204)


@tasks_router.delete("/", status_code=204)
async def delete_all_completed_tasks(db: DbSession):
    await db.execute(delete(Task).where(Task.is_checked))
    await db.commit()

    return Response(status_code=204)
