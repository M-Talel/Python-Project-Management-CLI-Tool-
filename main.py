# CLI Entry Point for Project Management Tool

import sys
from models.users import User
from models.projects import Project
from models.tasks import Task
from utils.storage import Storage
from rich.console import Console

# Initialize console for rich formatting
console = Console()
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
    console.print(help_message)


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
        console.print(f"[green]✓ User '{name}' added successfully![/green]")
    
    elif command == "list-users":
        users = storage.get_all_users()
        if not users:
            console.print("[yellow]No users found[/yellow]")
        else:
            console.print("\n[bold cyan]Users:[/bold cyan]")
            for user in users:
                console.print(f"  - {user.name} ({user.email})")
            console.print()
    
    elif command == "add-project" and len(args) == 4:
        user, title, description, due_date = args[0], args[1], args[2], args[3]
        project = Project(title=title, description=description, due_date=due_date)
        storage.add_project(user, project)
        console.print(f"[green]✓ Project '{title}' added to user '{user}'![/green]")
    
    elif command == "list-projects" and len(args) == 1:
        user = args[0]
        projects = storage.get_projects(user)
        if not projects:
            console.print(f"[yellow]No projects found for user '{user}'[/yellow]")
        else:
            console.print(f"\n[bold cyan]Projects for {user}:[/bold cyan]")
            for project in projects:
                console.print(f"  - {project.title}")
                console.print(f"    Description: {project.description}")
                console.print(f"    Due Date: {project.due_date}\n")
    
    elif command == "add-task" and len(args) == 4:
        project, title, status, assigned_to = args[0], args[1], args[2], args[3]
        task = Task(title=title, status=status, assigned_to=assigned_to)
        storage.add_task(project, task)
        console.print(f"[green]✓ Task '{title}' added to project '{project}'![/green]")
    
    elif command == "list-tasks" and len(args) == 1:
        project = args[0]
        tasks = storage.get_tasks(project)
        if not tasks:
            console.print(f"[yellow]No tasks found for project '{project}'[/yellow]")
        else:
            console.print(f"\n[bold cyan]Tasks for {project}:[/bold cyan]")
            for task in tasks:
                console.print(f"  - {task.title}")
                console.print(f"    Status: {task.status}")
                console.print(f"    Assigned to: {task.assigned_to}\n")
    
    elif command == "complete-task" and len(args) == 2:
        project, task_title = args[0], args[1]
        storage.update_task_status(project, task_title, "completed")
        console.print(f"[green]✓ Task '{task_title}' marked as completed![/green]")
    
    else:
        console.print("[red]✗ Invalid command or incorrect number of arguments[/red]")
        setup_parser()
