# Python Project Management CLI Tool

## Overview

A simple command-line tool to manage users, projects, and tasks with persistent JSON storage.

## Installation

No external (pip) dependencies are required.

Run the app from the project directory:

```bash
python3 main.py
```

## Usage

This project runs as an **interactive command-line menu** (it does not use subcommands/arguments).

Start the app:

```bash
python3 main.py
```

You will see a menu with options **1–8**:

1. Add a new user
2. List all users
3. Add a project
4. List projects for a user
5. Add a task
6. List tasks for a project
7. Mark task as completed
8. Exit

### What to enter (key prompts)

- **Add a project** asks for:
  - `Enter user name`
  - `Enter project title`
  - `Enter project description`
  - `Enter due date (YYYY-MM-DD)`

- **Add a task** asks for:
  - `Enter project name`
  - `Enter task title`
  - `Enter task status` (options shown in the app): `pending`, `in_progress`, `completed`
  - `Enter assigned user`

- **Mark a task as completed** asks for:
  - `Enter project name`
  - `Enter task title`

## Features

- User management
- Project creation and tracking
- Task assignment and status updates
- Persistent JSON file storage

## Project Structure

```
.
├── main.py              # CLI entry point
├── models/              # Data models
│   ├── users.py
│   ├── projects.py
│   └── tasks.py
├── utils/               # Storage functions
│   └── storage.py       # JSON file storage
└── data/                # Generated storage files
    ├── users.json
    ├── projects.json
    └── tasks.json
```

## Requirements

- Python 3.7+
