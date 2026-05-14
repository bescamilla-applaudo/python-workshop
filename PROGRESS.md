# PyForge — Workshop Progress

## Setup
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -e ".[dev]"`)
- [ ] `python main.py` works
- [ ] Sample data verified

---

## Phase 1 — Python Core: Data Model
- [ ] `pyforge/models.py` created with Copilot
- [ ] `Startup` dataclass with properties (age, funding_per_employee)
- [ ] Special methods implemented (__repr__, __eq__, __hash__)
- [ ] `AnalysisResult` dataclass created
- [ ] Validation executed successfully
- [ ] Compared with `solutions/pyforge/models.py`

## Phase 2 — OOP: Repository Pattern
- [ ] `pyforge/repository.py` created with Copilot
- [ ] Full CRUD (add, get, get_all, update, delete)
- [ ] Search and filters (search, filter_by_category, filter_by_profitable, sort_by)
- [ ] Special methods implemented (__len__, __contains__, __iter__)
- [ ] Validation executed successfully
- [ ] Compared with `solutions/pyforge/repository.py`

## Phase 3 — Pydantic: Validation and Analysis
- [ ] `pyforge/schemas.py` created with validators
- [ ] `pyforge/config.py` created with Settings
- [ ] `pyforge/analysis.py` created with analysis functions
- [ ] Positive validation works
- [ ] Negative validation rejects invalid data
- [ ] Compared with solutions

## Phase 4 — File I/O: Reading and Writing
- [ ] `pyforge/io/readers.py` created (CSV, JSON, auto-detect)
- [ ] `pyforge/io/writers.py` created (CSV, JSON, Markdown, auto-detect)
- [ ] Reads `data/startups.csv` correctly
- [ ] Reads `data/startups.json` correctly
- [ ] Exports to Markdown
- [ ] Compared with solutions

## Phase 5 — Advanced: Decorators & Pipeline
- [ ] `pyforge/decorators.py` created (@timer, @log_call, @retry, @validate_non_empty)
- [ ] `pyforge/pipeline.py` created with generators
- [ ] Transformations (add_funding_tier, normalize_country) work
- [ ] Full pipeline executed successfully
- [ ] Compared with solutions

## Phase 6 — Testing with pytest
- [ ] `tests/conftest.py` with shared fixtures
- [ ] `tests/test_models.py` — all pass
- [ ] `tests/test_schemas.py` — all pass
- [ ] `tests/test_repository.py` — all pass
- [ ] `tests/test_analysis.py` — all pass
- [ ] `tests/test_pipeline.py` — all pass
- [ ] `pytest tests/ -v` — all green
- [ ] Compared with solutions

## Phase 7 — CLI with Typer + Rich
- [ ] `pyforge/cli.py` created with commands (load, stats, convert, pipeline)
- [ ] `pyforge/__main__.py` created
- [ ] `main.py` updated
- [ ] `python -m pyforge --help` works
- [ ] `python -m pyforge load data/startups.csv` shows table
- [ ] `python -m pyforge stats data/startups.json` shows analysis
- [ ] `python -m pyforge convert data/startups.csv output/report.md` works
- [ ] `python -m pyforge pipeline data/startups.csv` works
- [ ] Compared with solutions
