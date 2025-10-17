from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a task within a project.

    Each task has an ID, title, description, status, and an optional deadline.
    Only valid statuses are: 'todo', 'doing', and 'done'.
    """
    MAX_NUMBER_OF_TASK = 50
    VALID_STATUS = ["todo", "doing", "done"]

    id: int
    title: str
    description: str
    status: str = field(default="todo")
    deadline: datetime | None = None

    def __post_init__(self) -> None:
        if self.status not in self.VALID_STATUS:
            valid = self.VALID_STATUS
            status = self.status
            raise ValueError(
                f"The status '{status}' is not valid. Only {valid}"
                )
