# TODO - Rubric upgrade (aim 85-90)

- [x] Refactor CLI to argparse with subcommands (keep interactive menu optional)

- [ ] Harden persistence in utils/storage.py (try/except, safe load/save)
- [ ] Improve OOP: introduce BaseModel/BaseEntity and use inheritance in User/Project/Task
- [ ] Add pytest test suite under tests/ for validation, storage, and some CLI handlers
- [ ] Add external dependency + dependency manifest (requirements.txt/pyproject.toml) and use it in code
- [ ] Update README with new CLI usage + dependency install
- [ ] Run mypy/formatting (optional) and run python -m pytest
