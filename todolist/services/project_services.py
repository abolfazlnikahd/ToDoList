from statics.statics import MAX_NUMBER_OF_PROJECT, projects
from models.project import Project


def create_project(name: str, description: str) -> None:
    """Create a new project.

    Validates the project name and description for duplicates and word limits
    before adding it to the list of projects.
    """
    if len(projects) >= MAX_NUMBER_OF_PROJECT:
        print("Error: The number of projects exceeds the allowed limit.")
        return
    if any(p.name == name for p in projects):
        print("Error: Duplicate project name")
        return
    if len(name.split()) > 30 or len(description.split()) > 150:
        print("Error: Word limit not respected.")
        return

    project = Project(id=len(projects) + 1, name=name, description=description)
    projects.append(project)
    print(f"Project '{name}' was successfully created.")


def edit_project(project_id: int, new_name: str, new_description: str) -> None:
    """Edit an existing project's name and description.

    Checks for duplicate names and word limits before updating the project.
    """
    for p in projects:
        if p.id == project_id:
            duplicate_exists = any(
                                    x.name == new_name and x.id != project_id
                                    for x in projects
            )
            if duplicate_exists:
                print("Error: Duplicate project name")
                return
            name_word_count = len(new_name.split())
            description_word_count = len(new_description.split())

            if name_word_count > 30 or description_word_count > 150:
                print("Error: Word limit not respected.")
                return
            p.name = new_name
            p.description = new_description
            print(f"Project '{p.name}' was edited.")
            return
    print("Project not found.")


def delete_project(project_id: int) -> None:
    """Delete a project by its ID.

    Removes the project and all its associated tasks from the list.
    """
    global projects
    before = len(projects)
    projects = [p for p in projects if p.id != project_id]
    if len(projects) < before:
        print(
            f"Project with ID {project_id} was deleted "
            "(all tasks were also deleted).")
    else:
        print("Project not found.")


def list_projects() -> None:
    """Print a list of all existing projects.

    Displays each project's ID, name, and description.
    """
    if not projects:
        print("There are no projects.")
        return
    print("List of projects:")
    for p in projects:
        print(f"[{p.id}] {p.name} - {p.description}")
