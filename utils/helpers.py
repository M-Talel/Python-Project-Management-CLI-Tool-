# Helper functions and utilities

# Validate email format
def validate_email(email):
    if "@" in email and "." in email:
        return True
    return False

# Validate date format (YYYY-MM-DD)
def validate_date(date_string):
    if len(date_string) == 10 and date_string.count("-") == 2:
        return True
    return False

# Format task status for display
def format_status(status):
    status_lower = status.lower()
    if status_lower == "completed":
        return "[green]✓ Completed[/green]"
    elif status_lower == "pending":
        return "[yellow]⏳ Pending[/yellow]"
    elif status_lower == "in progress":
        return "[blue]→ In Progress[/blue]"
    return status

# Get user input with prompt
def get_input(prompt):
    return input(prompt)
