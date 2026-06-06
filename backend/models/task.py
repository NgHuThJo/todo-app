from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(String(255), unique=True)
    is_checked: Mapped[bool] = mapped_column(default=False)

    def __init__(self, task: str, is_checked: bool = False):
        self.task = task
        self.is_checked = is_checked
