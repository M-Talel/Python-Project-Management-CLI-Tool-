from pathlib import Path

from utils.storage import Storage



class TmpStorage(Storage):
    """Storage that writes into a temp directory."""

    def __init__(self, tmp_path: Path):
        self.users_file = str(tmp_path / "users.json")
        self.projects_file = str(tmp_path / "projects.json")
        self.tasks_file = str(tmp_path / "tasks.json")
        self.create_data_folder()


def test_storage_recovers_empty_files(tmp_path):
    s = TmpStorage(tmp_path)

    assert s.get_all_users() == []
    assert s.get_projects("Any") == []
    assert s.get_tasks("Any") == []



def test_storage_add_user_and_persist(tmp_path):
    s = TmpStorage(tmp_path)

    from models.users import User

    s.add_user(User(name="Alice", email="alice@example.com"))

    s2 = TmpStorage(tmp_path)
    users = s2.get_all_users()
    assert len(users) == 1
    assert users[0].name == "Alice"


def test_storage_update_task_status(tmp_path):
    s = TmpStorage(tmp_path)

    from models.users import User
    from models.projects import Project
    from models.tasks import Task

    s.add_user(User(name="Alice", email="alice@example.com"))
    s.add_project("Alice", Project(title="P1", description="d", due_date="2026-12-31"))
    s.add_task("P1", Task(title="T1", status="pending", assigned_to="Alice"))

    updated = s.update_task_status("P1", "T1", "completed")
    assert updated is True

    tasks = s.get_tasks("P1")
    assert tasks[0].title == "T1"
    assert tasks[0].status == "completed"

