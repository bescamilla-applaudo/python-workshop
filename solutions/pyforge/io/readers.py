import csv
import json
from pathlib import Path

from ..models import Startup


def read_csv(file_path: str | Path) -> list[Startup]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected CSV file, got: {path.suffix}")

    startups: list[Startup] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            startup = Startup(
                id=int(row["id"]),
                name=row["name"],
                category=row["category"],
                funding_usd=float(row["funding_usd"]),
                employees=int(row["employees"]),
                founded_year=int(row["founded_year"]),
                country=row["country"],
                revenue_usd=float(row["revenue_usd"]),
                is_profitable=row["is_profitable"].lower() in ("true", "1", "yes"),
            )
            startups.append(startup)
    return startups


def read_json(file_path: str | Path) -> list[Startup]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix.lower() != ".json":
        raise ValueError(f"Expected JSON file, got: {path.suffix}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected a JSON array of startups")

    return [Startup(**item) for item in data]


def read_file(file_path: str | Path) -> list[Startup]:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return read_csv(path)
    elif suffix == ".json":
        return read_json(path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}. Use .csv or .json")
