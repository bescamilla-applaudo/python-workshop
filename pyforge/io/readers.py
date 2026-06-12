import csv
import json
from pathlib import Path

from pyforge.models import Startup


def _path(file_path: str | Path) -> Path:
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    return p


def _row_to_startup(row: dict) -> Startup:
    return Startup(
        id=int(row["id"]),
        name=row["name"],
        category=row["category"],
        funding_usd=float(row["funding_usd"]),
        employees=int(row["employees"]),
        founded_year=int(row["founded_year"]),
        country=row["country"],
        revenue_usd=float(row["revenue_usd"]),
        is_profitable=str(row["is_profitable"]).strip().lower() in ("true", "1", "yes"),
    )


def read_csv(file_path: str | Path) -> list[Startup]:
    p = _path(file_path)
    if p.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, got: {p.suffix!r}")
    with p.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return [_row_to_startup(row) for row in reader]


def read_json(file_path: str | Path) -> list[Startup]:
    p = _path(file_path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("JSON file must contain a top-level array")
    return [_row_to_startup(item) for item in data]


def read_file(file_path: str | Path) -> list[Startup]:
    p = _path(file_path)
    match p.suffix.lower():
        case ".csv":
            return read_csv(p)
        case ".json":
            return read_json(p)
        case _:
            raise ValueError(f"Unsupported file format: {p.suffix!r}. Use .csv or .json")
