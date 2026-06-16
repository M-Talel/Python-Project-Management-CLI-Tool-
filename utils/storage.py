# File I/O and storage functions

import json
import os
from models.users import User
from models.projects import Project
from models.tasks import Task


class Storage:
    # Initialize storage with file paths
    def __init__(self):
        self.users_file = "data/users.json"
        self.projects_file = "data/projects.json"
        self.tasks_file = "data/tasks.json"
        self.create_data_folder()
    
    # Create data folder if it doesn't exist
    def create_data_folder(self):
        if not os.path.exists("data"):
            os.makedirs("data")
    
    # Load all users from JSON file
    def get_all_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                data = json.load(f)
                return [User.from_dict(user) for user in data]
        return []
    
    # Save a new user to JSON file
    def add_user(self, user):
        users = self.get_all_users()
        users.append(user)
        with open(self.users_file, "w") as f:
            json.dump([u.to_dict() for u in users], f, indent=2)

    def user_exists(self, user_name):
        users = self.get_all_users()
        for u in users:
            if u.name == user_name:
                return True
        return False

    def get_user_by_name(self, user_name):
        users = self.get_all_users()
        for u in users:
            if u.name == user_name:
                return u
        return None

    
    # Load all projects from JSON file
    def get_all_projects(self):
        if os.path.exists(self.projects_file):
            with open(self.projects_file, "r") as f:
                data = json.load(f)
                return data
        return {}

    def project_exists(self, user_name, project_title):
        projects = self.get_projects(user_name)
        for p in projects:
            if p.title == project_title:
                return True
        return False

    def project_title_exists(self, project_title):
        projects_data = self.get_all_projects()
        for user_projects in projects_data.values():
            for p in user_projects:
                if p.get("title") == project_title:
                    return True
        return False

    def task_exists(self, project_name, task_title):
        tasks = self.get_tasks(project_name)
        for t in tasks:
            if t.title == task_title:
                return True
        return False

    
    # Get projects for a specific user
    def get_projects(self, user_name):
        projects_data = self.get_all_projects()
        if user_name in projects_data:
            return [Project.from_dict(p) for p in projects_data[user_name]]
        return []
    
    # Save a new project for a user
    def add_project(self, user_name, project):
        projects_data = self.get_all_projects()
        if user_name not in projects_data:
            projects_data[user_name] = []
        projects_data[user_name].append(project.to_dict())
        with open(self.projects_file, "w") as f:
            json.dump(projects_data, f, indent=2)
    
    # Load all tasks from JSON file
    def get_all_tasks(self):
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as f:
                data = json.load(f)
                return data
        return {}
    
    # Get tasks for a specific project
    def get_tasks(self, project_name):
        tasks_data = self.get_all_tasks()
        if project_name in tasks_data:
            return [Task.from_dict(t) for t in tasks_data[project_name]]
        return []
    
    # Save a new task for a project
    def add_task(self, project_name, task):
        tasks_data = self.get_all_tasks()
        if project_name not in tasks_data:
            tasks_data[project_name] = []
        tasks_data[project_name].append(task.to_dict())
        with open(self.tasks_file, "w") as f:
            json.dump(tasks_data, f, indent=2)
    
    # Update task status
    def update_task_status(self, project_name, task_title, new_status):
        tasks_data = self.get_all_tasks()
        updated = False
        if project_name in tasks_data:
            for task in tasks_data[project_name]:
                if task["title"] == task_title:
                    task["status"] = new_status
                    updated = True
        with open(self.tasks_file, "w") as f:
            json.dump(tasks_data, f, indent=2)
        return updated

