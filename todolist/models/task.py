from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    MAX_NUMBER_OF_TASK = 50
    VALID_STATUS = ["todo", "doing", "done"]

    id: int
    title: str
    description: str
    status: str = field(default="todo")
    deadline: datetime | None = None

    def __post_init__(self):
        if self.status not in self.VALID_STATUS:
            valid = self.VALID_STATUS
            status = self.status
            raise ValueError(f"وضعیت '{status}' معتبر نیست. فقط {valid}")
