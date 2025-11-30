from repositories.task_repository import TaskRepository
from repositories.project_repository import ProjectRepository
from models.task import Task
from exceptions import NotFoundError, ValidationError
from datetime import datetime
from config import MAX_NUMBER_OF_TASK

VALID_STATUS = ("todo", "doing", "done")


def _words_count_ok(s: str, max_words: int) -> bool:
    return len(s.split()) <= max_words


class TaskService:
    def __init__(self,
                 task_repo: TaskRepository,
                 project_repo: ProjectRepository):
        # Constructor Injection: repos injected from outside
        self.task_repo = task_repo
        self.project_repo = project_repo

    def add_task(self,
                 project_id: int,
                 title: str,
                 description: str = "",
                 deadline: datetime | None = None) -> Task:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found.")
        if len(project.tasks) >= MAX_NUMBER_OF_TASK:
            raise ValidationError("""Maximum number of
                                  tasks in project reached.""")
        if not _words_count_ok(title, 30):
            raise ValidationError("Title/description exceed word limits.")
        if not _words_count_ok(description or "", 150):
            raise ValidationError("Title/description exceed word limits.")
        if deadline and not isinstance(deadline, datetime):
            raise ValidationError("Deadline must be a datetime object.")

        task = Task(project_id=project_id,
                    title=title,
                    description=description,
                    status="todo",
                    deadline=deadline)
        self.task_repo.add(task)
        return task

    def edit_task(self,
                  project_id: int,
                  task_id: int,
                  title: str,
                  description: str,
                  status: str,
                  deadline: datetime | None = None) -> Task:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found.")
        task = self.task_repo.get_by_id(task_id)
        if not task or task.project_id != project_id:
            raise NotFoundError("Task not found in project.")
        if not _words_count_ok(title, 30):
            raise ValidationError("Title/description exceed word limits.")
        if not _words_count_ok(description or "", 150):
            raise ValidationError("Title/description exceed word limits.")
        if status not in VALID_STATUS:
            raise ValidationError("Invalid status.")
        task.title = title
        task.description = description
        task.status = status
        task.deadline = deadline
        if status == "done" and task.closed_at is None:
            task.closed_at = datetime.utcnow()
        return task

    def change_status(self,
                      project_id: int,
                      task_id: int,
                      new_status: str) -> Task:
        if new_status not in VALID_STATUS:
            raise ValidationError("Invalid status.")
        task = self.task_repo.get_by_id(task_id)
        if not task or task.project_id != project_id:
            raise NotFoundError("Task not found in project.")
        task.status = new_status
        if new_status == "done":
            task.closed_at = datetime.utcnow()
        return task

    def delete_task(self, project_id: int, task_id: int) -> None:
        task = self.task_repo.get_by_id(task_id)
        if not task or task.project_id != project_id:
            raise NotFoundError("Task not found in project.")
        self.task_repo.delete(task)

    def list_tasks(self, project_id: int):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found.")
        return self.task_repo.list_by_project(project_id)
