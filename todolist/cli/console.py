from todolist.db.session import SessionLocal
from todolist.repositories.project_repository import ProjectRepository
from todolist.repositories.task_repository import TaskRepository
from todolist.services.project_services import ProjectService
from todolist.services.task_services import TaskService
from datetime import datetime
from todolist.exceptions import NotFoundError, ValidationError


def run_cli():
    print("ToDoList CLI started. Ctrl+C to exit.")
    while True:
        try:
            print("""\n1. List projects\n
                        2. Create project\n
                  3. Delete project\n
                  4.Edit project\n
                  5. List tasks in project\n
                  6. Add task\n
                  7.Change task status\n
                  8.Edit task\n
                  9. Delete task\n
                  q. Quit""")
            choice = input("Choice: ").strip()
            if choice == "q":
                break

            db = SessionLocal()
            project_repo = ProjectRepository(db)
            task_repo = TaskRepository(db)
            psvc = ProjectService(project_repo)
            tsvc = TaskService(task_repo, project_repo)

            if choice == "1":
                projects = psvc.list_projects()
                if not projects:
                    print("No projects.")
                else:
                    for p in projects:
                        print(f"[{p.id}] {p.name} - {p.description}")

            elif choice == "2":
                name = input("Project name: ").strip()
                desc = input("Project description: ").strip()
                psvc.create_project(name, desc)
                db.commit()
                print("Project created.")

            elif choice == "3":
                pid = int(input("Project ID to delete: ").strip())
                psvc.delete_project(pid)
                db.commit()
                print("Project deleted.")

            elif choice == "4":
                pid = int(input("Project ID to edit: ").strip())
                new_name = input("New name: ").strip()
                new_desc = input("New description: ").strip()
                psvc.edit_project(pid, new_name, new_desc)
                db.commit()
                print("Project updated.")

            elif choice == "5":
                pid = int(input("Project ID: ").strip())
                tasks = tsvc.list_tasks(pid)
                if not tasks:
                    print("No tasks.")
                else:
                    for t in tasks:
                        if t.deadline:
                            dl = t.deadline.strftime("%Y-%m-%d")
                        else:
                            dl = "-"
                        print(
                            f"[{t.id}] {t.title} | {t.status} | deadline: {dl}"
                            )

            elif choice == "6":
                pid = int(input("Project ID to add task: ").strip())
                title = input("Title: ").strip()
                desc = input("Description: ").strip()
                dl = input("Deadline (YYYY-MM-DD) or empty: ").strip()
                dl_dt = datetime.strptime(dl, "%Y-%m-%d") if dl else None
                tsvc.add_task(pid, title, desc, dl_dt)
                db.commit()
                print("Task added.")

            elif choice == "7":
                pid = int(input("Project ID: ").strip())
                tid = int(input("Task ID: ").strip())
                status = input("New status (todo/doing/done): ").strip()
                tsvc.change_status(pid, tid, status)
                db.commit()
                print("Task status changed.")

            elif choice == "8":
                pid = int(input("Project ID: ").strip())
                tid = int(input("Task ID: ").strip())
                title = input("Title: ").strip()
                desc = input("Description: ").strip()
                status = input("Status (todo/doing/done): ").strip()
                dl = input("Deadline (YYYY-MM-DD) or empty: ").strip()
                dl_dt = datetime.strptime(dl, "%Y-%m-%d") if dl else None
                tsvc.edit_task(pid, tid, title, desc, status, dl_dt)
                db.commit()
                print("Task updated.")

            elif choice == "9":
                pid = int(input("Project ID: ").strip())
                tid = int(input("Task ID: ").strip())
                tsvc.delete_task(pid, tid)
                db.commit()
                print("Task deleted.")

            else:
                print("Invalid option.")

        except (ValidationError, NotFoundError) as e:
            db.rollback()
            print("Error:", str(e))
        except Exception as e:
            try:
                db.rollback()
            except Exception as d:
                print(d)
                pass
            print("Unexpected error:", str(e))
        finally:
            try:
                db.close()
            except Exception as d:
                print(d)
                pass
