# CLI Entry Point for Project Management Tool

import argparse
import sys

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="project-tool",
        description="Project Management CLI (users, projects, tasks) with persistent JSON storage.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # users
    users = sub.add_parser("users", help="Manage users")
    users_sub = users.add_subparsers(dest="users_command", required=True)

    users_add = users_sub.add_parser("add", help="Add a new user")
    users_add.add_argument("--name", required=True)
    users_add.add_argument("--email", required=True)

    users_list = users_sub.add_parser("list", help="List all users")

    # projects
    projects = sub.add_parser("projects", help="Manage projects")
    projects_sub = projects.add_subparsers(dest="projects_command", required=True)

    projects_add = projects_sub.add_parser("add", help="Add a project for a user")
    projects_add.add_argument("--user", required=True)
    projects_add.add_argument("--title", required=True)
    projects_add.add_argument("--description", required=True)
    projects_add.add_argument("--due-date", required=True)

    projects_list = projects_sub.add_parser("list", help="List projects for a user")
    projects_list.add_argument("--user", required=True)

    # tasks
    tasks = sub.add_parser("tasks", help="Manage tasks")
    tasks_sub = tasks.add_subparsers(dest="tasks_command", required=True)

    tasks_add = tasks_sub.add_parser("add", help="Add a task to a project")
    tasks_add.add_argument("--project", required=True)
    tasks_add.add_argument("--title", required=True)
    tasks_add.add_argument("--status", required=True, choices=["pending", "in_progress", "completed"])
    tasks_add.add_argument("--assigned-to", required=True)

    tasks_list = tasks_sub.add_parser("list", help="List tasks for a project")
    tasks_list.add_argument("--project", required=True)

    tasks_complete = tasks_sub.add_parser("complete", help="Mark a task as completed")
    tasks_complete.add_argument("--project", required=True)
    tasks_complete.add_argument("--title", required=True)

    return parser


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
    # CLI entry point (argparse) + interactive fallback
    parser = build_parser()

    # If the user provided no args, fall back to interactive menu.
    if len(sys.argv) == 1:
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
        return

    args = parser.parse_args()

    # Dispatch subcommands
    if args.command == "users":
        if args.users_command == "add":
            if not validate_email(args.email):
                print("\n✗ Invalid email format.")
                return
            if storage.user_exists(args.name):
                print(f"\n✗ User '{args.name}' already exists.")
                return
            storage.add_user(User(name=args.name, email=args.email))
            print(f"\n✓ User '{args.name}' added successfully!")
        elif args.users_command == "list":
            list_users()

    elif args.command == "projects":
        if args.projects_command == "add":
            if not storage.user_exists(args.user):
                print(f"\n✗ User '{args.user}' does not exist. Add the user first.")
                return
            if not validate_date_yyyy_mm_dd(args.due_date):
                print("\n✗ Invalid due date. Please enter in YYYY-MM-DD format.")
                return
            if storage.project_exists(args.user, args.title):
                print(f"\n✗ Project '{args.title}' already exists for user '{args.user}'.")
                return
            storage.add_project(args.user, Project(title=args.title, description=args.description, due_date=args.due_date))
            print(f"\n✓ Project '{args.title}' added to user '{args.user}'!")
        elif args.projects_command == "list":
            if not storage.user_exists(args.user):
                print(f"\n✗ User '{args.user}' does not exist.")
                return
            projects = storage.get_projects(args.user)
            if not projects:
                print(f"\nNo projects found for user '{args.user}'")
            else:
                print(f"\n--- Projects for {args.user} ---")
                for project in projects:
                    print(
                        f"  • {project.title}\n"
                        f"    Description: {project.description}\n"
                        f"    Due Date: {project.due_date}"
                    )

    elif args.command == "tasks":
        if args.tasks_command == "add":
            if not storage.project_title_exists(args.project):
                print(f"\n✗ Project '{args.project}' does not exist. Add the project first.")
                return
            if not validate_task_status(args.status):
                print("\n✗ Invalid status. Allowed: pending, in_progress, completed")
                return
            if not storage.user_exists(args.assigned_to):
                print(f"\n✗ Assigned user '{args.assigned_to}' does not exist.")
                return
            if storage.task_exists(args.project, args.title):
                print(f"\n✗ Task '{args.title}' already exists for project '{args.project}'.")
                return
            storage.add_task(
                args.project,
                Task(title=args.title, status=args.status, assigned_to=args.assigned_to),
            )
            print(f"\n✓ Task '{args.title}' added to project '{args.project}'!")

        elif args.tasks_command == "list":
            if not storage.project_title_exists(args.project):
                print(f"\n✗ Project '{args.project}' does not exist.")
                return
            tasks = storage.get_tasks(args.project)
            if not tasks:
                print(f"\nNo tasks found for project '{args.project}'")
            else:
                print(f"\n--- Tasks for {args.project} ---")
                for task in tasks:
                    print(
                        f"  • {task.title}\n"
                        f"    Status: {task.status}\n"
                        f"    Assigned to: {task.assigned_to}"
                    )

        elif args.tasks_command == "complete":
            if not storage.project_title_exists(args.project):
                print(f"\n✗ Project '{args.project}' does not exist.")
                return
            if not storage.task_exists(args.project, args.title):
                print(f"\n✗ Task '{args.title}' does not exist in project '{args.project}'.")
                return
            updated = storage.update_task_status(args.project, args.title, "completed")
            if updated:
                print(f"\n✓ Task '{args.title}' marked as completed!")
            else:
                print("\n✗ Could not update the task status.")


if __name__ == "__main__":
    main()

