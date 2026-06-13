# Project class definition

class Project:
    # Initialize a new project
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []
    
    # String representation of project
    def __str__(self):
        return f"Project: {self.title} (Due: {self.due_date})"
    
    # Add a task to this project
    def add_task(self, task):
        if task not in self.tasks:
            self.tasks.append(task)
    
    # Get all tasks for this project
    def get_tasks(self):
        return self.tasks
    
    # Convert project to dictionary for JSON storage
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date
        }
    
    # Create project from dictionary
    @staticmethod
    def from_dict(data):
        return Project(data["title"], data["description"], data["due_date"])
