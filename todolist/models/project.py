from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from .task import Task


MAX_NUMBER_OF_PROJECT = 10


@dataclass
class Project:
    """Represents a project that contains multiple tasks.

    Each project has an ID, name, description, creation date,
    and a list of tasks. Supports adding and deleting tasks.
    """
    id: int
    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        if len(self.tasks) >= Task.MAX_NUMBER_OF_TASK:
            raise ValueError("The number of tasks exceeds the allowed limit.")
        self.tasks.append(task)

    def delete_task(self, task_id: int) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]
