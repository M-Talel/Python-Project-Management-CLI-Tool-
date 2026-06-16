import json
import os
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class JsonLoadResult:
    data: Any
    used_fallback: bool


def _atomic_write(path: str, content: str, encoding: str = "utf-8") -> None:
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)

    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding=encoding) as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())

    os.replace(tmp_path, path)


def load_json(path: str, default: Any) -> JsonLoadResult:
    """Load JSON from `path`.

    - If missing: return default.
    - If invalid/corrupt: return default.
    - Never raises JSONDecodeError to callers.
    """

    if not os.path.exists(path):
        return JsonLoadResult(data=default, used_fallback=True)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return JsonLoadResult(data=json.load(f), used_fallback=False)
    except json.JSONDecodeError:
        return JsonLoadResult(data=default, used_fallback=True)
    except OSError:
        return JsonLoadResult(data=default, used_fallback=True)


def save_json(path: str, data: Any) -> None:
    """Atomic JSON save."""

    content = json.dumps(data, indent=2)
    _atomic_write(path, content)

