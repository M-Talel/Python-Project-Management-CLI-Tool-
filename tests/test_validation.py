from utils.validation import validate_date_yyyy_mm_dd, validate_email, validate_task_status, require_non_blank


def test_require_non_blank():
    assert require_non_blank("x") is True
    assert require_non_blank("  y  ") is True
    assert require_non_blank("") is False
    assert require_non_blank(None) is False


def test_validate_email():
    assert validate_email("a@b.com") is True
    assert validate_email("a@b") is False
    assert validate_email("@b.com") is False
    assert validate_email("") is False


def test_validate_task_status():
    assert validate_task_status("pending") is True
    assert validate_task_status("in_progress") is True
    assert validate_task_status("completed") is True
    assert validate_task_status("done") is False
    assert validate_task_status("") is False


def test_validate_date_yyyy_mm_dd():
    assert validate_date_yyyy_mm_dd("2026-12-31") is True
    assert validate_date_yyyy_mm_dd("2026/12/31") is False
    assert validate_date_yyyy_mm_dd("2026-1-01") is False
    assert validate_date_yyyy_mm_dd("1899-01-01") is False
    assert validate_date_yyyy_mm_dd("2026-13-01") is False
    assert validate_date_yyyy_mm_dd("2026-00-01") is False

