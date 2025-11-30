from repositories.project_repository import ProjectRepository
from models.project import Project
from config import MAX_NUMBER_OF_PROJECT
from exceptions import NotFoundError, ValidationError


def _words_count_ok(s: str, max_words: int) -> bool:
    return len(s.split()) <= max_words


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def create_project(self, name: str, description: str) -> Project:
        # validations (business rules)
        if len(self.repo.list_all()) >= MAX_NUMBER_OF_PROJECT:
            raise ValidationError("Maximum number of projects reached.")
        if not _words_count_ok(name, 30):
            raise ValidationError("Name/description exceed word limits.")
        if not _words_count_ok(description or "", 150):
            raise ValidationError("Name/description exceed word limits.")
        if self.repo.get_by_name(name):
            raise ValidationError("Project name already exists.")

        proj = Project(name=name, description=description)
        self.repo.add(proj)
        return proj

    def edit_project(self,
                     project_id: int,
                     new_name: str,
                     new_description: str) -> Project:
        proj = self.repo.get_by_id(project_id)
        if not proj:
            raise NotFoundError("Project not found.")
        if not _words_count_ok(new_name, 30):
            raise ValidationError("Name/description exceed word limits.")
        if not _words_count_ok(new_description or "", 150):
            raise ValidationError("Name/description exceed word limits.")
        existing = self.repo.get_by_name(new_name)
        if existing and existing.id != project_id:
            raise ValidationError("Another project with this name exists.")
        proj.name = new_name
        proj.description = new_description
        return proj

    def delete_project(self, project_id: int) -> None:
        proj = self.repo.get_by_id(project_id)
        if not proj:
            raise NotFoundError("Project not found.")
        self.repo.delete(proj)

    def list_projects(self):
        return self.repo.list_all()

    def get_project(self, project_id: int) -> Project:
        proj = self.repo.get_by_id(project_id)
        if not proj:
            raise NotFoundError("Project not found.")
        return proj
