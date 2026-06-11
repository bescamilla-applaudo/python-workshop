# Python Workshop — AI-First Python from Zero

Hands-on workshop to learn **modern Python** from zero using AI as your copilot. You'll build **PyForge**, a startup data analyzer with a professional CLI.

## What you'll learn

- Dataclasses and type hints (modern Python)
- OOP with the Repository pattern
- Validation with Pydantic v2
- File I/O: CSV, JSON, Markdown
- Decorators and generators (advanced patterns)
- Testing with pytest (fixtures, assertions, conftest)
- CLI with Typer + Rich (formatted tables in the terminal)

## Prerequisites

- Python 3.11+
- VS Code with GitHub Copilot
- Basic terminal knowledge

## Setup

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -e ".[dev]"

# 3. Verify
python main.py
# → "PyForge v0.1.0"
```

## Structure

| Folder | Purpose |
|---|---|
| `pyforge/` | Your work — you build the package module by module |
| `data/` | Sample data (CSV and JSON with 20 startups) |
| `tests/` | Your work — tests with pytest |
| `solutions/` | Complete reference (do not modify) |

## How to use

1. Open [INSTRUCTIONS.md](INSTRUCTIONS.md) — it has ready-made prompts for Copilot Chat
2. Follow the phases in order (1→7)
3. Each phase has validation with real commands
4. If you get stuck, check `solutions/`

## Quick commands

```bash
source .venv/bin/activate              # Activate environment
python -m pyforge --help               # View CLI commands
python -m pyforge load data/startups.csv   # Load data
python -m pyforge stats data/startups.json # Statistics
pytest tests/ -v                       # Run tests
```

## Theoretical reference

See [PYTHON.md](PYTHON.md) for in-depth concepts.
