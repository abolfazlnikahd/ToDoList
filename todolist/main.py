from services.project_services import (
    create_project,
    list_projects,
    delete_project,
    edit_project,
)
from services.task_services import (
    add_task,
    change_task_status,
    list_tasks,
    delete_task,
    edit_task
)


if __name__ == "__main__":
    print("The program has started. Press Ctrl+C to exit.\n")

    try:
        while True:
            user_input = input(
                "-------------------\n"
                "\n"
                "how can i help?\n"
                "1. List of your projects\n"
                "2. Create a new project.\n"
                "3. Remove a project.\n"
                "4. Edit a project.\n"
                "5. Show all tasks in a project.\n"
                "6. Add a task.\n"
                "7. Change the status of the task.\n"
                "8. Edit a task.\n"
                "9. Remove a task.\n"
                "\n"
                "-------------------\n"
                ).strip()

            if user_input == "1":
                list_projects()

            elif user_input == "2":
                name = input("Project name: ").strip()
                description = input("Project description: ").strip()
                create_project(name, description)

            elif user_input == "3":
                project_id = int(input("Project ID to delete: ").strip())
                delete_project(project_id)

            elif user_input == "4":
                project_id = int(input("Project ID to edit: ").strip())
                new_name = input("New project name: ").strip()
                new_description = input("New project description: ").strip()
                edit_project(project_id, new_name, new_description)

            elif user_input == "5":
                project_id = int(input("Project ID: ").strip())
                list_tasks(project_id)

            elif user_input == "6":
                project_id = int(input("Project ID to add a task: ").strip())
                title = input("Task title: ").strip()
                description = input("Task description: ").strip()
                deadline = input(
                                "Deadline (YYYY-MM-DD) or leave empty: "
                                ).strip()
                deadline = deadline if deadline else None
                add_task(project_id, title, description, deadline)

            elif user_input == "7":
                project_id = int(input("Project ID: ").strip())
                task_id = int(input("Task ID: ").strip())
                status = input("New status (todo/doing/done): ").strip()
                change_task_status(project_id, task_id, status)

            elif user_input == "8":
                project_id = int(input("Project ID: ").strip())
                task_id = int(input("Task ID: ").strip())
                title = input("New task title: ").strip()
                description = input("New task description: ").strip()
                status = input("New status (todo/doing/done): ").strip()
                deadline = input(
                                "New deadline (YYYY-MM-DD) or leave empty: "
                                ).strip()
                deadline = deadline if deadline else None
                edit_task(
                    project_id,
                    task_id,
                    title,
                    description,
                    status,
                    deadline
                    )

            elif user_input == "9":
                project_id = int(input("Project ID: ").strip())
                task_id = int(input("Task ID: ").strip())
                delete_task(project_id, task_id)

            else:
                print("Invalid option. Please try again.")
    except KeyboardInterrupt:
        print("The program has been closed.")
