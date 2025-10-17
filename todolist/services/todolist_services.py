from models.project import Project


class ToDoListService:
    def __init__(self):
        self.projects: list[Project] = []

    def add_project(self, project_name: str):
        if self.get_project(project_name):
            raise ValueError("Project already exists.")
        project = Project(project_name)
        self.projects.append(project)
        return project

    def remove_project(self, project_name: str):
        self.projects = [p for p in self.projects if p.name != project_name]

    def get_project(self, project_name: str):
        for p in self.projects:
            if p.name == project_name:
                return p
        return None

    def list_projects(self):
        return self.projects
