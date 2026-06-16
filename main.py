# CLI Entry Point for Project Management Tool

from models.users import User
from models.projects import Project
from models.tasks import Task
from utils.storage import Storage

storage = Storage()


def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("PROJECT MANAGEMENT TOOL")
    print("="*50)
    print("\n1. Add a new user")
    print("2. List all users")
    print("3. Add a project")
    print("4. List projects for a user")
    print("5. Add a task")
    print("6. List tasks for a project")
    print("7. Mark task as completed")
    print("8. Exit")
    print("\n" + "="*50)


def add_user():
    """Add a new user"""
    name = input("Enter user name: ").strip()
    email = input("Enter user email: ").strip()
    
    if name and email:
        user = User(name=name, email=email)
        storage.add_user(user)
        print(f"\n✓ User '{name}' added successfully!")
    else:
        print("\n✗ Invalid input. Please try again.")


def list_users():
    #List the users in the system
    users = storage.get_all_users()
    if not users:
        print("\nNo users found")
    else:
        print("\n--- Users ---")
        for user in users:
            print(f"  • {user.name} ({user.email})")
    print()


def add_project():
    #Adds a new project
    user = input("Enter user name: ").strip()
    title = input("Enter project title: ").strip()
    description = input("Enter project description: ").strip()
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()
    
    if user and title and description and due_date:
        project = Project(title=title, description=description, due_date=due_date)
        storage.add_project(user, project)
        print(f"\n✓ Project '{title}' added to user '{user}'!")
    else:
        print("\n✗ Invalid input. Please try again.")


def list_projects():
    #List projects for a user
    user = input("Enter user name: ").strip()
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
    #Add a task to a project
    project = input("Enter project name: ").strip()
    title = input("Enter task title: ").strip()
    print("Task status options: pending, in_progress, completed")
    status = input("Enter task status: ").strip()
    assigned_to = input("Enter assigned user: ").strip()
    
    if project and title and status and assigned_to:
        task = Task(title=title, status=status, assigned_to=assigned_to)
        storage.add_task(project, task)
        print(f"\n✓ Task '{title}' added to project '{project}'!")
    else:
        print("\n✗ Invalid input. Please try again.")


def list_tasks():
    #List tasks for a project
    project = input("Enter project name: ").strip()
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
    #Mark a task as completed
    project = input("Enter project name: ").strip()
    task_title = input("Enter task title: ").strip()
    
    if project and task_title:
        storage.update_task_status(project, task_title, "completed")
        print(f"\n✓ Task '{task_title}' marked as completed!")
    else:
        print("\n✗ Invalid input. Please try again.")


def main():
    #Main loop for the interactive menu
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
