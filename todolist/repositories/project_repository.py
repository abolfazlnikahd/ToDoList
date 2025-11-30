from typing import List, Optional
from sqlalchemy.orm import Session
from models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, project: Project) -> Project:
        self.db.add(project)
        self.db.flush()  # so id is available
        return project

    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self.db.get(Project, project_id)

    def get_by_name(self, name: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.name == name).first()

    def list_all(self) -> List[Project]:
        return self.db.query(Project).order_by(Project.created_at).all()

    def delete(self, project: Project) -> None:
        self.db.delete(project)
