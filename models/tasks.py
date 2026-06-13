# Task class definition

class Task:
    # Initialize a new task
    def __init__(self, title, status, assigned_to):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
    
    # String representation of task
    def __str__(self):
        return f"Task: {self.title} [{self.status}]"
    
    # Update task status
    def update_status(self, new_status):
        self.status = new_status
    
    # Convert task to dictionary for JSON storage
    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to
        }
    
    # Create task from dictionary
    @staticmethod
    def from_dict(data):
        return Task(data["title"], data["status"], data["assigned_to"])
