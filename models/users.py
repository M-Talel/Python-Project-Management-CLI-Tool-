# User class definition

class User:
    # Initialize a new user
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.projects = []
    
    # String representation of user
    def __str__(self):
        return f"User: {self.name} ({self.email})"
    
    # Add a project to this user
    def add_project(self, project):
        if project not in self.projects:
            self.projects.append(project)
    
    # Get all projects for this user
    def get_projects(self):
        return self.projects
    
    # Convert user to dictionary for JSON storage
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email
        }
    
    # Create user from dictionary
    @staticmethod
    def from_dict(data):
        return User(data["name"], data["email"])
