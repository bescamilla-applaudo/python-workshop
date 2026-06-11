import csv
import json
from dataclasses import asdict
from pathlib import Path

from ..models import Startup


def write_csv(startups: list[Startup], file_path: str | Path) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not startups:
        raise ValueError("No data to write")

    fieldnames = list(asdict(startups[0]).keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for startup in startups:
            writer.writerow(asdict(startup))


def write_json(startups: list[Startup], file_path: str | Path) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = [asdict(s) for s in startups]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_markdown(startups: list[Startup], file_path: str | Path) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not startups:
        raise ValueError("No data to write")

    headers = [
        "ID", "Name", "Category", "Funding (USD)",
        "Employees", "Country", "Profitable",
    ]

    lines: list[str] = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for s in startups:
        row = [
            str(s.id),
            s.name,
            s.category,
            f"${s.funding_usd:,.0f}",
            str(s.employees),
            s.country,
            "Yes" if s.is_profitable else "No",
        ]
        lines.append("| " + " | ".join(row) + " |")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def export(startups: list[Startup], file_path: str | Path) -> None:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        write_csv(startups, path)
    elif suffix == ".json":
        write_json(startups, path)
    elif suffix == ".md":
        write_markdown(startups, path)
    else:
        raise ValueError(f"Unsupported format: {suffix}. Use .csv, .json, or .md")
