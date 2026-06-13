# Python Project Management CLI Tool

A simple command-line application to manage users, projects, and tasks with JSON-based data persistence.

## Features

- **User Management**: Add and view users with name and email
- **Project Management**: Create projects for users with description and due dates
- **Task Management**: Add tasks to projects with status tracking (pending, in progress, completed)
- **Data Persistence**: All data automatically saved to JSON files
- **Simple CLI**: Easy-to-use command-line interface with colored output

## Project Structure

```
Summative_Lab/
├── main.py                    # CLI entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .gitignore
│
├── models/                    # Data model classes
│   ├── users.py              # User class
│   ├── projects.py           # Project class
│   └── tasks.py              # Task class
│
├── utils/                     # Utility functions
│   ├── storage.py            # JSON file I/O and Storage class
│   └── helpers.py            # Helper functions
│
└── data/                      # Data storage (auto-created)
    ├── users.json
    ├── projects.json
    └── tasks.json
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Summative_Lab
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Display Help
```bash
python3 main.py
```

### User Commands

**Add a new user:**
```bash
python3 main.py add-user <name> <email>
```
Example:
```bash
python3 main.py add-user Alex alex@example.com
```

**List all users:**
```bash
python3 main.py list-users
```

### Project Commands

**Add a new project:**
```bash
python3 main.py add-project <user> <title> <description> <due_date>
```
Example:
```bash
python3 main.py add-project Alex "CLI Tool" "Build CLI application" 2026-12-31
```

**List projects for a user:**
```bash
python3 main.py list-projects <user>
```
Example:
```bash
python3 main.py list-projects Alex
```

### Task Commands

**Add a new task:**
```bash
python3 main.py add-task <project> <title> <status> <assigned_to>
```
Example:
```bash
python3 main.py add-task "CLI Tool" "Implement add-user" pending Alex
```

**List tasks for a project:**
```bash
python3 main.py list-tasks <project>
```
Example:
```bash
python3 main.py list-tasks "CLI Tool"
```

**Mark a task as completed:**
```bash
python3 main.py complete-task <project> <task_title>
```
Example:
```bash
python3 main.py complete-task "CLI Tool" "Implement add-user"
```

## Class Structure

### User Class
- **Attributes**: name, email, projects list
- **Methods**: add_project(), get_projects(), to_dict(), from_dict()

### Project Class
- **Attributes**: title, description, due_date, tasks list
- **Methods**: add_task(), get_tasks(), to_dict(), from_dict()

### Task Class
- **Attributes**: title, status, assigned_to
- **Methods**: update_status(), to_dict(), from_dict()

### Storage Class
- Handles all JSON file operations
- Methods: add_user(), get_all_users(), add_project(), get_projects(), add_task(), get_tasks(), update_task_status()

## Data Format

### users.json
```json
[
  {
    "name": "Alex",
    "email": "alex@example.com"
  }
]
```

### projects.json
```json
{
  "Alex": [
    {
      "title": "CLI Tool",
      "description": "Build CLI application",
      "due_date": "2026-12-31"
    }
  ]
}
```

### tasks.json
```json
{
  "CLI Tool": [
    {
      "title": "Implement add-user",
      "status": "pending",
      "assigned_to": "Alex"
    }
  ]
}
```

## Sample Data

The project includes sample data with:
- 3 sample users: Alex, Jordan, Morgan
- 4 sample projects across users
- 9 sample tasks with various status states

Run `python3 main.py list-users` to see the sample data.

## Dependencies

- **rich** (v13.0.0+): For colored terminal output and formatted display

## Known Issues

- Projects and tasks are organized by name (not ID), so duplicate names may cause issues
- Email validation is basic
- Date format must be YYYY-MM-DD

## Future Enhancements

- Add database support (SQLite, PostgreSQL)
- Implement user authentication
- Add email notifications
- Create a GUI interface
- Add project categories and filters
- Implement task priorities
- Add due date reminders

## Testing

To test the application, run the CLI commands with the sample data:

```bash
python3 main.py list-users
python3 main.py list-projects Alex
python3 main.py list-tasks "CLI Tool"
```

## License

This project is part of the Summative Lab assessment.

## Author

Created as part of Python Programming Course Assessment
