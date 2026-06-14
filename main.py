# CLI Entry Point for Project Management Tool

import sys
from models.users import User
from models.projects import Project
from models.tasks import Task
from utils.storage import Storage

storage = Storage()


def setup_parser():
    # Display help message with available commands
    help_message = """
Project Management CLI - Available Commands:

1. add-user <name> <email>
   Example: python main.py add-user Alex alex@example.com

2. list-users
   Example: python main.py list-users

3. add-project <user> <title> <description> <due_date>
   Example: python main.py add-project Alex "CLI Tool" "Build CLI" 2026-12-31

4. list-projects <user>
   Example: python main.py list-projects Alex

5. add-task <project> <title> <status> <assigned_to>
   Example: python main.py add-task "CLI Tool" "Implement add-task" pending Alex

6. list-tasks <project>
   Example: python main.py list-tasks "CLI Tool"

7. complete-task <project> <task_title>
   Example: python main.py complete-task "CLI Tool" "Implement add-task"
    """
    print(help_message)


def parse_command():
    # Parse command from sys.argv
    if len(sys.argv) < 2:
        setup_parser()
        return None, None
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    return command, args


if __name__ == "__main__":
    # Main entry point - parse arguments and execute appropriate command
    command, args = parse_command()
    
    if command is None:
        sys.exit(0)
    
    elif command == "add-user" and len(args) == 2:
        name, email = args[0], args[1]
        user = User(name=name, email=email)
        storage.add_user(user)
        print(f"User '{name}' added successfully!")
    
    elif command == "list-users":
        users = storage.get_all_users()
        if not users:
            print("No users found")
        else:
            print("\nUsers:")
            for user in users:
                print(f"  - {user.name} ({user.email})")
            print()
    
    elif command == "add-project" and len(args) == 4:
        user, title, description, due_date = args[0], args[1], args[2], args[3]
        project = Project(title=title, description=description, due_date=due_date)
        storage.add_project(user, project)
        print(f"Project '{title}' added to user '{user}'!")
    
    elif command == "list-projects" and len(args) == 1:
        user = args[0]
        projects = storage.get_projects(user)
        if not projects:
            print(f"No projects found for user '{user}'")
        else:
            print(f"\nProjects for {user}:")
            for project in projects:
                print(f"  - {project.title}")
                print(f"    Description: {project.description}")
                print(f"    Due Date: {project.due_date}")
    
    elif command == "add-task" and len(args) == 4:
        project, title, status, assigned_to = args[0], args[1], args[2], args[3]
        task = Task(title=title, status=status, assigned_to=assigned_to)
        storage.add_task(project, task)
        print(f"Task '{title}' added to project '{project}'!")
    
    elif command == "list-tasks" and len(args) == 1:
        project = args[0]
        tasks = storage.get_tasks(project)
        if not tasks:
            print(f"No tasks found for project '{project}'")
        else:
            print(f"\nTasks for {project}:")
            for task in tasks:
                print(f"  - {task.title}")
                print(f"    Status: {task.status}")
                print(f"    Assigned to: {task.assigned_to}")
    
    elif command == "complete-task" and len(args) == 2:
        project, task_title = args[0], args[1]
        storage.update_task_status(project, task_title, "completed")
        print(f"Task '{task_title}' marked as completed!")
    
    else:
        print("Invalid command or incorrect number of arguments")
        setup_parser()
