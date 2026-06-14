# Python Project Management CLI Tool

## Overview

A simple command-line tool to manage users, projects, and tasks with persistent JSON storage.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### User Management

```bash
# Add a new user
python main.py add-user Alice alice@example.com

# List all users
python main.py list-users
```

### Project Management

```bash
# Add a project for a user
python main.py add-project Alice "Website Redesign" "Redesign company website" 2026-12-31

# List projects for a user
python main.py list-projects Alice
```

### Task Management

```bash
# Add a task to a project
python main.py add-task "Website Redesign" "Design mockups" pending Alice

# List tasks for a project
python main.py list-tasks "Website Redesign"

# Mark a task as completed
python main.py complete-task "Website Redesign" "Design mockups"
```

## Features

- ✓ User management with email validation
- ✓ Project creation and tracking
- ✓ Task assignment and status updates
- ✓ Persistent JSON file storage
- ✓ Rich CLI formatting with colors and icons

## Project Structure

```
.
├── main.py              # CLI entry point
├── models/              # Data models
│   ├── users.py
│   ├── projects.py
│   └── tasks.py
├── utils/               # Utility functions
│   ├── helpers.py       # Validation and formatting
│   └── storage.py       # JSON file storage
└── data/                # Generated storage files
    ├── users.json
    ├── projects.json
    └── tasks.json
```

## Requirements

- Python 3.7+
- rich (for terminal formatting)
