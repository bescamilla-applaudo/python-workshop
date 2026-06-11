# PyForge — Startup Data Analyzer CLI
## AI-First Workshop: Python from Zero to Professional

> **Methodology:** You don't write code from scratch. You ask Copilot to generate it, run it, and understand what was generated. Each phase includes the exact prompt you should use.
>
> **Theoretical reference:** Check `PYTHON.md` when you need to understand a concept in depth.

---

## Initial Setup

### 1. Create virtual environment
```bash
cd python-workshop
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -e ".[dev]"
```

### 3. Verify it works
```bash
python main.py
# Should print: PyForge v0.1.0
```

### 4. Verify sample data
```bash
head -5 data/startups.csv
python3 -c "import json; data=json.load(open('data/startups.json')); print(f'{len(data)} startups')"
```

---

## Project Structure (what you'll build)

```
python-workshop/
├── main.py                  ← entry point (already exists)
├── pyproject.toml           ← dependencies
├── data/
│   ├── startups.csv         ← sample data
│   └── startups.json
├── pyforge/                 ← your package (empty at the start)
│   ├── __init__.py
│   ├── models.py            ← Phase 1: @dataclass
│   ├── repository.py        ← Phase 2: OOP
│   ├── schemas.py           ← Phase 3: Pydantic
│   ├── config.py            ← Phase 3: Settings
│   ├── analysis.py          ← Phase 3: data analysis
│   ├── io/
│   │   ├── readers.py       ← Phase 4: CSV/JSON reading
│   │   └── writers.py       ← Phase 4: CSV/JSON/MD writing
│   ├── decorators.py        ← Phase 5: decorators
│   ├── pipeline.py          ← Phase 5: generators
│   ├── cli.py               ← Phase 7: Typer CLI
│   └── __main__.py          ← Phase 7: python -m pyforge
└── tests/
    ├── conftest.py           ← Phase 6: fixtures
    ├── test_models.py        ← Phase 6
    ├── test_schemas.py       ← Phase 6
    ├── test_repository.py    ← Phase 6
    ├── test_analysis.py      ← Phase 6
    └── test_pipeline.py      ← Phase 6
```

---

## Phase 1 — Python Core: Data Model with @dataclass

**Context:** You'll create the project's central data model using `@dataclass`, the modern way to define data classes in Python. A dataclass automatically generates the constructor, representation, and comparison — you write the structure, Python generates the behavior.

### Prompt for Copilot

```
Create a file pyforge/models.py with a @dataclass called Startup that has the fields: id (int), name (str), category (str), funding_usd (float), employees (int), founded_year (int), country (str), revenue_usd (float), is_profitable (bool).

Add properties for: age (years from founded_year to today) and funding_per_employee (funding/employees, return 0.0 if employees is 0).

Implement __repr__ that shows id, name, and category. Implement __eq__ that compares by id. Implement __hash__ based on id.

Also create a @dataclass AnalysisResult with fields: total_startups (int), total_funding (float), avg_funding (float), avg_employees (int), categories (dict[str, int]), profitable_count (int), profitable_percentage (float).
```

### Validation

```bash
python3 -c "
from pyforge.models import Startup, AnalysisResult
s = Startup(1, 'TestCo', 'saas', 1000000, 50, 2020, 'US', 500000, True)
print(s)
print(f'Age: {s.age}, Per employee: {s.funding_per_employee}')
print(f'Hash: {hash(s)}')
s2 = Startup(1, 'Other', 'ai', 0, 0, 2020, 'US', 0, False)
print(f'Equal: {s == s2}')
"
```

### What to understand after this phase
- `@dataclass` generates `__init__`, `__repr__`, `__eq__` automatically — avoids writing boilerplate.
- `@property` is a computed getter — accessed like an attribute but executes a function.
- `__repr__`, `__eq__`, `__hash__` are "dunder methods" (double underscore) — they define how Python treats the object internally.

### Compare with the solution
```bash
diff pyforge/models.py solutions/pyforge/models.py
```

---

## Phase 2 — OOP: Repository Pattern

**Context:** Now you'll create a class that manages a collection of Startups in memory. You'll use the Repository pattern, which encapsulates data access behind a clean interface — tomorrow you could change the implementation to a database without touching the rest of the code.

### Prompt for Copilot

```
Create pyforge/repository.py with a StartupRepository class that manages startups in memory using an internal dict[int, Startup].

Required methods:
- add(startup) → Startup: adds to dict. If startup.id == 0, assigns auto-incrementing.
- get(startup_id) → Startup | None
- get_all() → list[Startup]
- update(startup_id, **kwargs) → Startup | None: updates fields with setattr
- delete(startup_id) → bool
- search(query) → list[Startup]: searches by name (case-insensitive)
- filter_by_category(category) → list[Startup]
- filter_by_profitable(profitable=True) → list[Startup]
- sort_by(field, reverse=False) → list[Startup]: sorts by any field

Special methods:
- __len__: number of startups
- __contains__: checks if an id exists
- __iter__: iterates over startups
```

### Validation

```bash
python3 -c "
from pyforge.models import Startup
from pyforge.repository import StartupRepository

repo = StartupRepository()
repo.add(Startup(1, 'Alpha', 'fintech', 5000000, 50, 2020, 'US', 1000000, False))
repo.add(Startup(2, 'Beta', 'saas', 20000000, 200, 2018, 'DE', 8000000, True))

print(f'Total: {len(repo)}')
print(f'Contains 1: {1 in repo}')
print(f'Search alpha: {repo.search(\"alpha\")}')
print(f'Profitable: {repo.filter_by_profitable(True)}')
print(f'Sorted: {[s.name for s in repo.sort_by(\"funding_usd\", reverse=True)]}')
"
```

### What to understand after this phase
- `**kwargs` receives named arguments as a dictionary — enables flexible functions without rigid signatures.
- `setattr(obj, key, value)` assigns attributes dynamically — useful for partial updates.
- `__contains__` allows using `in` with your object — `1 in repo` calls `repo.__contains__(1)`.

### Compare with the solution
```bash
diff pyforge/repository.py solutions/pyforge/repository.py
```

---

## Phase 3 — Pydantic: Validation and Analysis

**Context:** Pydantic validates data with declarative schemas — you define the expected structure and Pydantic rejects anything that doesn't comply. FastAPI uses it internally. In this phase you'll also create the analysis functions that operate on the data.

### Prompt for Copilot (schemas)

```
Create pyforge/schemas.py with Pydantic v2 models:

1. VALID_CATEGORIES = ["fintech", "healthtech", "edtech", "saas", "ecommerce", "ai", "other"]

2. StartupCreate(BaseModel):
   - name: str (min 2, max 200) with field_validator that rejects whitespace
   - category: str with field_validator that normalizes to lowercase and validates against VALID_CATEGORIES
   - funding_usd: float (>= 0)
   - employees: int (>= 1)
   - founded_year: int (>= 1900) with field_validator that rejects future years
   - country: str (min 2, max 100)
   - revenue_usd: float (default 0.0, >= 0)
   - is_profitable: bool (default False)

3. StartupResponse(BaseModel): all fields + id, with model_config from_attributes

4. StartupUpdate(BaseModel): all fields optional (str | None), with category validator

5. StartupFilter(BaseModel): category, min_funding, max_funding, min_employees, country, is_profitable — all optional
```

### Prompt for Copilot (config)

```
Create pyforge/config.py with a Settings class using pydantic-settings:
- data_dir: str = "data"
- output_format: str = "json"
- max_results: int = 100
- debug: bool = False
- env_prefix: "PYFORGE_"
- reads from .env file

Include a get_settings() function with @lru_cache.
```

### Prompt for Copilot (analysis)

```
Create pyforge/analysis.py with analysis functions that receive list[Startup]:

- analyze(startups) → AnalysisResult: calculates totals, averages, count by category, profitability
- top_funded(startups, n=5) → list[Startup]: top N by funding
- by_country(startups) → dict[str, list[Startup]]: groups by country
- funding_by_category(startups) → dict[str, float]: sums funding by category
- filter_startups(startups, category?, min_funding?, max_funding?, min_employees?, country?, is_profitable?) → list[Startup]: combined filter
```

### Validation

```bash
python3 -c "
from pyforge.schemas import StartupCreate
# Valid
s = StartupCreate(name='TestCo', category='FINTECH', funding_usd=1000000, employees=10, founded_year=2022, country='US')
print(f'Valid: {s.name}, category={s.category}')

# Invalid
try:
    StartupCreate(name='', category='invalid', funding_usd=-1, employees=0, founded_year=2099, country='')
except Exception as e:
    print(f'Error (expected): {e}')
"
```

### What to understand after this phase
- `field_validator` transforms or rejects an individual field before the model is constructed.
- `@lru_cache` memoizes the result of a function — the first call executes, subsequent ones return the cache.
- Comprehensions (`[x for x in items if cond]`) are the idiomatic way to filter and transform lists in Python.

### Compare with the solution
```bash
diff pyforge/schemas.py solutions/pyforge/schemas.py
diff pyforge/config.py solutions/pyforge/config.py
diff pyforge/analysis.py solutions/pyforge/analysis.py
```

---

## Phase 4 — File I/O: Reading and Writing

**Context:** Python handles files with `open()` and context managers (`with`). You'll read CSV and JSON, and export to multiple formats including Markdown.

### Prompt for Copilot (readers)

```
Create pyforge/io/__init__.py (empty) and pyforge/io/readers.py with:

- read_csv(file_path: str | Path) → list[Startup]: reads CSV with csv.DictReader, validates it exists and is .csv
- read_json(file_path: str | Path) → list[Startup]: reads JSON, validates it's a list
- read_file(file_path: str | Path) → list[Startup]: auto-detects format by extension

Use pathlib.Path for everything. Raise FileNotFoundError if it doesn't exist and ValueError if the format is unsupported.
```

### Prompt for Copilot (writers)

```
Create pyforge/io/writers.py with:

- write_csv(startups, file_path): writes CSV with csv.DictWriter using dataclasses.asdict
- write_json(startups, file_path): writes JSON with indent=2
- write_markdown(startups, file_path): writes Markdown table with formatted headers
- export(startups, file_path): auto-detects format by extension (.csv, .json, .md)

Create the parent directory if it doesn't exist (path.parent.mkdir). Raise ValueError if the list is empty.
```

### Validation

```bash
python3 -c "
from pyforge.io.readers import read_file
startups = read_file('data/startups.csv')
print(f'CSV: {len(startups)} startups loaded')
print(f'First: {startups[0]}')

startups_json = read_file('data/startups.json')
print(f'JSON: {len(startups_json)} startups loaded')
"
```

```bash
python3 -c "
from pyforge.io.readers import read_file
from pyforge.io.writers import export
startups = read_file('data/startups.csv')
export(startups, 'output/startups.md')
print('Exported to Markdown')
" && head -5 output/startups.md
```

### What to understand after this phase
- `with open()` is a context manager — guarantees the file is closed, like an automatic `try-finally`.
- `csv.DictReader` converts each row into a dict — like parsing a CSV into objects in JS.
- `dataclasses.asdict()` converts a dataclass to a dict — like `JSON.stringify()` but for Python objects.

### Compare with the solution
```bash
diff pyforge/io/readers.py solutions/pyforge/io/readers.py
diff pyforge/io/writers.py solutions/pyforge/io/writers.py
```

---

## Phase 5 — Advanced: Decorators & Pipeline

> **Switch the model → Claude Sonnet 4.6 or GPT-5.4**
> Decorators with `ParamSpec`, `TypeVar`, and `@wraps` require precise reasoning about Python's type system.
> Gemini 3 Flash often generates decorators that lose the original signature or don't preserve types correctly.

**Context:** Decorators are one of Python's most powerful features — used in FastAPI (`@app.get`), pytest (`@pytest.fixture`), and LangGraph. Generators allow processing data as a stream without loading everything into memory.

### Prompt for Copilot (decorators)

```
Create pyforge/decorators.py with decorators using functools.wraps, ParamSpec, and TypeVar:

1. @timer: measures execution time with time.perf_counter, logs with logging.info
2. @log_call: logs the call and result (or error if it fails)
3. @retry(max_attempts=3, delay=1.0): retries the function N times with delay between attempts
4. @validate_non_empty: validates that arguments of type list, dict, or str are not empty, raises ValueError

Use logging.getLogger("pyforge") for all logs.
```

### Prompt for Copilot (pipeline)

```
Create pyforge/pipeline.py with a generator-based pipeline:

1. read_records(data: list[dict]) → Generator[dict]: yield each record
2. validate_records(records) → Generator[dict]: validates with StartupCreate, prints warning and skips invalid
3. transform_records(records, transformations?) → Generator[dict]: applies list of transformation functions
4. collect(records) → list[dict]: materializes the generator
5. run_pipeline(data, transformations?) → list[dict]: orchestrates the entire pipeline

Transformation functions:
- add_funding_tier(record) → dict: adds "funding_tier" (Pre-seed/Seed/Series A-B/Series C+)
- normalize_country(record) → dict: normalizes US→United States, UK→United Kingdom
```

### Validation

```bash
python3 -c "
from pyforge.decorators import timer, retry

@timer
def slow_function():
    total = sum(range(1000000))
    return total

import logging
logging.basicConfig(level=logging.INFO)
result = slow_function()
print(f'Result: {result}')
"
```

```bash
python3 -c "
from pyforge.io.readers import read_file
from pyforge.pipeline import run_pipeline, add_funding_tier, normalize_country
from dataclasses import asdict

startups = read_file('data/startups.csv')
raw = [asdict(s) for s in startups]
results = run_pipeline(raw, transformations=[add_funding_tier, normalize_country])
print(f'Processed: {len(results)} records')
for r in results[:3]:
    print(f'  {r[\"name\"]}: {r.get(\"funding_tier\", \"?\")}')
"
```

### What to understand after this phase
- A decorator is a function that receives a function and returns a function — `@timer` is syntactic sugar for `slow_function = timer(slow_function)`.
- `@wraps(func)` preserves the original function's name and docstring — without this, debugging breaks.
- `ParamSpec` and `TypeVar` preserve the original's types — the decorator doesn't lose the decorated function's signature.
- `yield` creates a generator — produces values one at a time on demand instead of loading everything into memory.

### Compare with the solution
```bash
diff pyforge/decorators.py solutions/pyforge/decorators.py
diff pyforge/pipeline.py solutions/pyforge/pipeline.py
```

---

## Phase 6 — Testing with pytest

**Context:** pytest is the standard testing framework in Python. Fixtures are functions that prepare data or state before each test — they're injected by name, shared via `conftest.py`, and can be composed together.

### Prompt for Copilot

```
Create complete tests for PyForge in tests/:

tests/conftest.py:
- Fixture sample_startup: a single test Startup
- Fixture sample_startups: list of 5 startups with varied data (fintech, saas, ai, edtech, healthtech)
- Fixture repo: StartupRepository pre-loaded with sample_startups

tests/test_models.py:
- Test creation, age property, funding_per_employee, zero employees, equality, inequality, hash, repr

tests/test_schemas.py:
- Test valid creation, category normalization, invalid category, negative funding, future year, empty name, zero employees, partial update, filter

tests/test_repository.py:
- Test add/get, get nonexistent, get_all, update, update nonexistent, delete, delete nonexistent, search, search case-insensitive, filter_by_category, filter_by_profitable, sort_by, len, contains, iter

tests/test_analysis.py:
- Test analyze, analyze empty, top_funded, by_country, funding_by_category, filter combined

tests/test_pipeline.py:
- Test pipeline basic, skips invalid, with transformations, add_funding_tier tiers, normalize_country, empty input
```

### Validation

```bash
pytest tests/ -v
```

**All tests must pass.**

### What to understand after this phase
- Fixtures are injected by name — pytest looks for them in `conftest.py` automatically.
- `pytest.raises(ValidationError)` verifies that a code block raises exactly that error type.
- Each test is independent — pytest creates fresh fixtures for each test.

### Compare with the solution
```bash
diff -r tests/ solutions/tests/
```

---

## Phase 7 — CLI with Typer + Rich

**Context:** Typer is the "FastAPI for CLIs" — it uses type hints to generate the command-line interface. Rich is the library for beautiful terminal output (tables, colors, formatting).

### Prompt for Copilot

```
Create pyforge/cli.py with a Typer app that has these commands:

1. load <file_path>: loads data and shows a Rich table with columns ID, Name, Category, Funding, Employees, Country, Profitable

2. stats <file_path>: shows complete analysis — totals, averages, profitability, by category, top 5 funded, funding by category

3. convert <input_path> <output_path>: converts between formats (CSV↔JSON↔Markdown)

4. pipeline <file_path>: runs the pipeline with add_funding_tier and normalize_country, shows tier distribution

Use rich.console.Console for output and rich.table.Table for tables.

Also create pyforge/__main__.py that imports and runs the app so you can run python -m pyforge.

Update main.py to import and run the CLI.
```

### Validation

```bash
# Help
python -m pyforge --help

# Load data
python -m pyforge load data/startups.csv

# Statistics
python -m pyforge stats data/startups.json

# Convert formats
python -m pyforge convert data/startups.csv output/report.md
cat output/report.md

# Pipeline
python -m pyforge pipeline data/startups.csv
```

### What to understand after this phase
- `typer.Argument(...)` is like required params of a FastAPI endpoint.
- `rich.Table` lets you create formatted tables in the terminal — with colors, alignment, and styles.
- `__main__.py` allows running the package as a module: `python -m pyforge`.

### Compare with the solution
```bash
diff pyforge/cli.py solutions/pyforge/cli.py
```

---

## Quick Commands

| Action | Command |
|---|---|
| Activate venv | `source .venv/bin/activate` |
| Install deps | `pip install -e ".[dev]"` |
| Run starter | `python main.py` |
| Run CLI | `python -m pyforge --help` |
| Load data | `python -m pyforge load data/startups.csv` |
| Statistics | `python -m pyforge stats data/startups.json` |
| Convert format | `python -m pyforge convert data/startups.csv output/report.md` |
| Pipeline | `python -m pyforge pipeline data/startups.csv` |
| Run tests | `pytest tests/ -v` |
| Tests with coverage | `pytest tests/ -v --cov=pyforge` |
| Compare with solution | `diff -r pyforge/ solutions/pyforge/` |

---

## Tips for Copilot (Gemini 3 Flash)

1. **Be specific in prompts** — include field names, types, and expected behavior.
2. **One module per prompt** — don't ask for the entire project at once.
3. **Ask for the complete file** — "create file X" works better than "modify file X".
4. **If the code doesn't work**, paste the full error and ask "fix this error".
5. **To understand something**, ask "explain what X does with a practical example".

---

## Progress

Check `PROGRESS.md` and mark each completed phase. When you finish a phase, tell Copilot:

> "Review PROGRESS.md and let's continue with the next phase."
