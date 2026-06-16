# CLI Entry Point for Project Management Tool

from models.users import User
from models.projects import Project
from models.tasks import Task
from utils.storage import Storage
from utils.validation import (
    validate_date_yyyy_mm_dd,
    validate_email,
    validate_task_status,
    require_non_blank,
)

storage = Storage()


def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("PROJECT MANAGEMENT TOOL")
    print("=" * 50)
    print("\n1. Add a new user")
    print("2. List all users")
    print("3. Add a project")
    print("4. List projects for a user")
    print("5. Add a task")
    print("6. List tasks for a project")
    print("7. Mark task as completed")
    print("8. Exit")
    print("\n" + "=" * 50)


def add_user():
    """Add a new user"""
    name = input("Enter user name: ").strip()
    email = input("Enter user email: ").strip()

    if not require_non_blank(name) or not require_non_blank(email):
        print("\n✗ Invalid input. Name and email are required.")
        return

    if not validate_email(email):
        print("\n✗ Invalid email format. Please try again.")
        return

    if storage.user_exists(name):
        print(f"\n✗ User '{name}' already exists.")
        return

    user = User(name=name, email=email)
    storage.add_user(user)
    print(f"\n✓ User '{name}' added successfully!")


def list_users():
    # List the users in the system
    users = storage.get_all_users()
    if not users:
        print("\nNo users found")
    else:
        print("\n--- Users ---")
        for user in users:
            print(f"  • {user.name} ({user.email})")
    print()


def add_project():
    # Adds a new project
    user = input("Enter user name: ").strip()
    title = input("Enter project title: ").strip()
    description = input("Enter project description: ").strip()
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()

    if not require_non_blank(user) or not require_non_blank(title) or not require_non_blank(description) or not require_non_blank(due_date):
        print("\n✗ Invalid input. All project fields are required.")
        return

    if not storage.user_exists(user):
        print(f"\n✗ User '{user}' does not exist. Add the user first.")
        return

    if not validate_date_yyyy_mm_dd(due_date):
        print("\n✗ Invalid due date. Please enter in YYYY-MM-DD format.")
        return

    # Project titles are per-user (projects.json is grouped by user)
    if storage.project_exists(user, title):
        print(f"\n✗ Project '{title}' already exists for user '{user}'.")
        return

    project = Project(title=title, description=description, due_date=due_date)
    storage.add_project(user, project)
    print(f"\n✓ Project '{title}' added to user '{user}'!")


def list_projects():
    # List projects for a user
    user = input("Enter user name: ").strip()

    if not require_non_blank(user):
        print("\n✗ Invalid input. User name is required.")
        return

    if not storage.user_exists(user):
        print(f"\n✗ User '{user}' does not exist.")
        return

    projects = storage.get_projects(user)

    if not projects:
        print(f"\nNo projects found for user '{user}'")
    else:
        print(f"\n--- Projects for {user} ---")
        for project in projects:
            print(f"  • {project.title}")
            print(f"    Description: {project.description}")
            print(f"    Due Date: {project.due_date}")
    print()


def add_task():
    # Add a task to a project
    project = input("Enter project name: ").strip()
    title = input("Enter task title: ").strip()
    print("Task status options: pending, in_progress, completed")
    status = input("Enter task status: ").strip()
    assigned_to = input("Enter assigned user: ").strip()

    if not require_non_blank(project) or not require_non_blank(title) or not require_non_blank(status) or not require_non_blank(assigned_to):
        print("\n✗ Invalid input. All task fields are required.")
        return

    if not storage.project_title_exists(project):
        print(f"\n✗ Project '{project}' does not exist. Add the project first.")
        return

    if not validate_task_status(status):
        print("\n✗ Invalid status. Allowed: pending, in_progress, completed")
        return

    if not storage.user_exists(assigned_to):
        print(f"\n✗ Assigned user '{assigned_to}' does not exist.")
        return

    if storage.task_exists(project, title):
        print(f"\n✗ Task '{title}' already exists for project '{project}'.")
        return

    task = Task(title=title, status=status, assigned_to=assigned_to)
    storage.add_task(project, task)
    print(f"\n✓ Task '{title}' added to project '{project}'!")


def list_tasks():
    # List tasks for a project
    project = input("Enter project name: ").strip()

    if not require_non_blank(project):
        print("\n✗ Invalid input. Project name is required.")
        return

    if not storage.project_title_exists(project):
        print(f"\n✗ Project '{project}' does not exist.")
        return

    tasks = storage.get_tasks(project)

    if not tasks:
        print(f"\nNo tasks found for project '{project}'")
    else:
        print(f"\n--- Tasks for {project} ---")
        for task in tasks:
            print(f"  • {task.title}")
            print(f"    Status: {task.status}")
            print(f"    Assigned to: {task.assigned_to}")
    print()


def complete_task():
    # Mark a task as completed
    project = input("Enter project name: ").strip()
    task_title = input("Enter task title: ").strip()

    if not require_non_blank(project) or not require_non_blank(task_title):
        print("\n✗ Invalid input. Project name and task title are required.")
        return

    if not storage.project_title_exists(project):
        print(f"\n✗ Project '{project}' does not exist.")
        return

    if not storage.task_exists(project, task_title):
        print(f"\n✗ Task '{task_title}' does not exist in project '{project}'.")
        return

    updated = storage.update_task_status(project, task_title, "completed")
    if updated:
        print(f"\n✓ Task '{task_title}' marked as completed!")
    else:
        print("\n✗ Could not update the task status.")


def main():
    # Main loop for the interactive menu
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            add_project()
        elif choice == "4":
            list_projects()
        elif choice == "5":
            add_task()
        elif choice == "6":
            list_tasks()
        elif choice == "7":
            complete_task()
        elif choice == "8":
            print("\nGoodbye!")
            break
        else:
            print("\n✗ Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()

