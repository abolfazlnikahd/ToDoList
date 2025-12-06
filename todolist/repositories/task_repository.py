from typing import List, Optional
from sqlalchemy.orm import Session
from todolist.models.task import Task
from datetime import datetime


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, task: Task) -> Task:
        self.db.add(task)
        self.db.flush()
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.get(Task, task_id)

    def list_by_project(self, project_id: int) -> List[Task]:
        query = self.db.query(Task).filter(Task.project_id == project_id)
        return query.order_by(Task.created_at).all()

    def delete(self, task: Task) -> None:
        self.db.delete(task)

    def list_overdue(self, now: datetime):
        return (
            self.db.query(Task)
            .filter(
                Task.deadline.is_not(None),
                Task.deadline < now,
                Task.status != "done"
            )
            .all()
        )
