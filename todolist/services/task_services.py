from datetime import datetime


from models.task import Task
from statics.statics import projects


def add_task(
    project_id: int,
    title: str,
    description: str,
    deadline: str | None = None
) -> None:
    """Add a new task to a specific project.

    Validates word limits, deadline format, and task count before adding.
    """
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    if len(project.tasks) >= Task.MAX_NUMBER_OF_TASK:
        print(" Error: The number of tasks exceeds the allowed limit.")
        return
    if len(title.split()) > 30 or len(description.split()) > 150:
        print(" Error: Word limit not respected.")
        return

    deadline_dt = None
    if deadline:
        try:
            deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            print("Date format is not valid. (Example: 2025-10-17)")
            return

    task = Task(
            id=len(project.tasks) + 1,
            title=title,
            description=description,
            deadline=deadline_dt)
    project.tasks.append(task)
    print(f"Task '{title}' added to project '{project.name}'.")


def edit_task(
        project_id: int,
        task_id: int,
        title: str,
        description: str,
        status: str,
        deadline: str | None = None
        ) -> None:
    """Edit an existing task in a project.

    Updates task details such as title, description, status, and deadline.
    Validates inputs before applying changes.
    """
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    task = next((t for t in project.tasks if t.id == task_id), None)
    if not task:
        print("Task not found.")
        return

    if len(title.split()) > 30 or len(description.split()) > 150:
        print("Word limit not respected.")
        return
    if status not in Task.VALID_STATUS:
        print(
            f"Status '{status}' is not valid. "
            f"Only one of {Task.VALID_STATUS}"
            )
        return

    deadline_dt = None
    if deadline:
        try:
            deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            print("The date format is not valid.")
            return

    task.title = title
    task.description = description
    task.status = status
    task.deadline = deadline_dt
    print(f"Task '{task.title}' was edited.")


def change_task_status(project_id: int, task_id: int, new_status: str) -> None:
    """Change the status of a specific task in a project.

    Ensures the new status is valid before updating the task.
    """
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    task = next((t for t in project.tasks if t.id == task_id), None)
    if not task:
        print("Task not found.")
        return

    if new_status not in Task.VALID_STATUS:
        print("The status is invalid.")
        return

    task.status = new_status
    print(f"ask status '{task.title}' changed to '{new_status}'.")


def delete_task(project_id: int, task_id: int) -> None:
    """Delete a specific task from a project by its ID.

    Removes the task if found; otherwise prints an error message.
    """
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    before = len(project.tasks)
    project.tasks = [t for t in project.tasks if t.id != task_id]
    if len(project.tasks) < before:
        print(f"Task {task_id} was deleted.")
    else:
        print("Task not found.")


def list_tasks(project_id: int) -> None:
    """List all tasks in a specific project.

    Displays task ID, title, status, and deadline for each task.
    """
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    if not project.tasks:
        print("There are no tasks in this project.")
        return

    print(f"Tasks for the project '{project.name}':")
    for t in project.tasks:
        deadline = t.deadline.strftime("%Y-%m-%d") if t.deadline else "-"
        print(f"[{t.id}] {t.title} | {t.status} | deadline: {deadline}")
