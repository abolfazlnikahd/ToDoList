from datetime import datetime
from db.session import SessionLocal
from repositories.task_repository import TaskRepository
from repositories.project_repository import ProjectRepository

def autoclose_overdue():
    db = SessionLocal()
    try:
        task_repo = TaskRepository(db)
        now = datetime.utcnow()
        overdue = task_repo.list_overdue(now)
        for t in overdue:
            t.status = "done"
            t.closed_at = datetime.utcnow()
        db.commit()
        print(f"Autoclosed {len(overdue)} tasks.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    autoclose_overdue()
