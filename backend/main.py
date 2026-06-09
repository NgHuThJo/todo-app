import uuid

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from sqlalchemy.exc import SQLAlchemyError
from structlog.contextvars import bind_contextvars, clear_contextvars

from features.tasks import tasks_router
from shared.logging import setup_logging

setup_logging()
logger: structlog.stdlib.BoundLogger = structlog.get_logger()

app = FastAPI()

origins = [
    "http://localhost:5173",
]


@app.exception_handler(SQLAlchemyError)
async def sql_alchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.exception("Database error", exc_info=exc._message)

    return JSONResponse(status_code=500, content={"detail": "Database error"})


@app.middleware("http")
async def setup_logging_context(request: Request, call_next):
    clear_contextvars()

    request_id = str(uuid.uuid4())
    bind_contextvars(
        path=request.url.path, method=request.method, request_id=request_id
    )

    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tasks_router)


def use_route_names_as_operation_ids(app: FastAPI):
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)
