from datetime import datetime, timezone
from todolist.db.session import SessionLocal
from todolist.repositories.task_repository import TaskRepository


def autoclose_overdue():
    db = SessionLocal()
    try:
        task_repo = TaskRepository(db)
        now = datetime.now(timezone.utc)
        overdue = task_repo.list_overdue(now)
        for t in overdue:
            t.status = "done"
            t.closed_at = datetime.now(timezone.utc)
        db.commit()
        print(f"Autoclosed {len(overdue)} tasks.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    autoclose_overdue()
