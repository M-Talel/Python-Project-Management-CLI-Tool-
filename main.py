"""
CLI Entry Point for Project Management Tool
Handles all CLI commands and user interactions
"""

import argparse
import sys
from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import Storage
from rich.console import Console
from rich.table import Table

# Initialize console for rich formatting
console = Console()
storage = Storage()


def add_user(args):
    """
    Add a new user to the system
    """
    try:
        user = User(name=args.name, email=args.email)
        storage.add_user(user)
        console.print(f"[green]✓ User '{args.name}' added successfully![/green]")
    except Exception as e:
        console.print(f"[red]✗ Error adding user: {e}[/red]")


def list_users(args):
    """
    Display all users in a formatted table
    """
    try:
        users = storage.get_all_users()
        if not users:
            console.print("[yellow]No users found[/yellow]")
            return
        
        table = Table(title="Users")
        table.add_column("Name", style="cyan")
        table.add_column("Email", style="magenta")
        
        for user in users:
            table.add_row(user.name, user.email)
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]✗ Error listing users: {e}[/red]")


def add_project(args):
    """
    Add a new project to a user
    """
    try:
        project = Project(title=args.title, description=args.description, due_date=args.due_date)
        storage.add_project(args.user, project)
        console.print(f"[green]✓ Project '{args.title}' added to user '{args.user}'![/green]")
    except Exception as e:
        console.print(f"[red]✗ Error adding project: {e}[/red]")


def list_projects(args):
    """
    Display all projects for a user
    """
    try:
        projects = storage.get_projects(args.user)
        if not projects:
            console.print(f"[yellow]No projects found for user '{args.user}'[/yellow]")
            return
        
        table = Table(title=f"Projects for {args.user}")
        table.add_column("Title", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Due Date", style="magenta")
        
        for project in projects:
            table.add_row(project.title, project.description, project.due_date)
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]✗ Error listing projects: {e}[/red]")


def add_task(args):
    """
    Add a new task to a project
    """
    try:
        task = Task(title=args.title, status=args.status, assigned_to=args.assigned_to)
        storage.add_task(args.project, task)
        console.print(f"[green]✓ Task '{args.title}' added to project '{args.project}'![/green]")
    except Exception as e:
        console.print(f"[red]✗ Error adding task: {e}[/red]")


def list_tasks(args):
    """
    Display all tasks for a project
    """
    try:
        tasks = storage.get_tasks(args.project)
        if not tasks:
            console.print(f"[yellow]No tasks found for project '{args.project}'[/yellow]")
            return
        
        table = Table(title=f"Tasks for {args.project}")
        table.add_column("Title", style="cyan")
        table.add_column("Status", style="yellow")
        table.add_column("Assigned To", style="magenta")
        
        for task in tasks:
            table.add_row(task.title, task.status, task.assigned_to)
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]✗ Error listing tasks: {e}[/red]")


def complete_task(args):
    """
    Mark a task as complete
    """
    try:
        storage.update_task_status(args.project, args.task_title, "completed")
        console.print(f"[green]✓ Task '{args.task_title}' marked as completed![/green]")
    except Exception as e:
        console.print(f"[red]✗ Error completing task: {e}[/red]")


def setup_parser():
    """
    Configure argparse with all CLI subcommands
    """
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py add-user --name "Alex" --email "alex@example.com"
  python main.py list-users
  python main.py add-project --user "Alex" --title "CLI Tool" --description "Build CLI" --due_date "2026-12-31"
  python main.py list-projects --user "Alex"
  python main.py add-task --project "CLI Tool" --title "Implement add-task" --status "pending" --assigned_to "Alex"
  python main.py list-tasks --project "CLI Tool"
  python main.py complete-task --project "CLI Tool" --task_title "Implement add-task"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # User commands
    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("--name", required=True, help="User's name")
    add_user_parser.add_argument("--email", required=True, help="User's email")
    add_user_parser.set_defaults(func=add_user)
    
    list_users_parser = subparsers.add_parser("list-users", help="List all users")
    list_users_parser.set_defaults(func=list_users)
    
    # Project commands
    add_project_parser = subparsers.add_parser("add-project", help="Add a new project")
    add_project_parser.add_argument("--user", required=True, help="User's name")
    add_project_parser.add_argument("--title", required=True, help="Project title")
    add_project_parser.add_argument("--description", default="", help="Project description")
    add_project_parser.add_argument("--due_date", default="", help="Project due date (YYYY-MM-DD)")
    add_project_parser.set_defaults(func=add_project)
    
    list_projects_parser = subparsers.add_parser("list-projects", help="List projects for a user")
    list_projects_parser.add_argument("--user", required=True, help="User's name")
    list_projects_parser.set_defaults(func=list_projects)
    
    # Task commands
    add_task_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_task_parser.add_argument("--project", required=True, help="Project title")
    add_task_parser.add_argument("--title", required=True, help="Task title")
    add_task_parser.add_argument("--status", default="pending", help="Task status")
    add_task_parser.add_argument("--assigned_to", default="", help="Assigned to (user name)")
    add_task_parser.set_defaults(func=add_task)
    
    list_tasks_parser = subparsers.add_parser("list-tasks", help="List tasks for a project")
    list_tasks_parser.add_argument("--project", required=True, help="Project title")
    list_tasks_parser.set_defaults(func=list_tasks)
    
    complete_task_parser = subparsers.add_parser("complete-task", help="Mark task as completed")
    complete_task_parser.add_argument("--project", required=True, help="Project title")
    complete_task_parser.add_argument("--task_title", required=True, help="Task title to complete")
    complete_task_parser.set_defaults(func=complete_task)
    
    return parser


if __name__ == "__main__":
    """
    Main entry point - parse arguments and execute appropriate command
    """
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    args.func(args)
