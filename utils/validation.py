# Validation helpers for the CLI tool


def validate_email(email):
    """Return True if `email` looks like an email address."""

    if not email:
        return False
    if "@" not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    if not parts[0] or not parts[1]:
        return False
    # Very small/naive check: domain must contain a dot
    if "." not in parts[1]:
        return False
    return True


def validate_task_status(status):
    if not status:
        return False
    allowed = ["pending", "in_progress", "completed"]
    if status not in allowed:
        return False
    return True


def validate_date_yyyy_mm_dd(date_str):
    if not date_str:
        return False
    if len(date_str) != 10:
        return False
    if date_str[4] != "-" or date_str[7] != "-":
        return False
    yyyy = date_str[0:4]
    mm = date_str[5:7]
    dd = date_str[8:10]

    if not (yyyy.isdigit() and mm.isdigit() and dd.isdigit()):
        return False

    year = int(yyyy)
    month = int(mm)
    day = int(dd)

    if year < 1900 or year > 2100:
        return False
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False

    return True


def require_non_blank(value):
    """Return True if `value` is a non-empty string (after stripping)."""

    if value is None:
        return False
    if not isinstance(value, str):
        return False
    if not value.strip():
        return False
    return True



