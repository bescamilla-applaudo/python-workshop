import csv
import json
from dataclasses import asdict
from pathlib import Path

from pyforge.models import Startup

_FIELDNAMES = [
    "id", "name", "category", "funding_usd", "employees",
    "founded_year", "country", "revenue_usd", "is_profitable",
]


def _prepare(startups: list[Startup], file_path: str | Path) -> Path:
    if not startups:
        raise ValueError("Cannot export an empty list of startups")
    p = Path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def write_csv(startups: list[Startup], file_path: str | Path) -> None:
    p = _prepare(startups, file_path)
    with p.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=_FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for startup in startups:
            writer.writerow(asdict(startup))


def write_json(startups: list[Startup], file_path: str | Path) -> None:
    p = _prepare(startups, file_path)
    p.write_text(
        json.dumps([asdict(s) for s in startups], indent=2),
        encoding="utf-8",
    )


def write_markdown(startups: list[Startup], file_path: str | Path) -> None:
    p = _prepare(startups, file_path)
    headers = ["ID", "Name", "Category", "Funding (USD)", "Employees",
               "Founded", "Country", "Revenue (USD)", "Profitable"]
    separator = ["---"] * len(headers)

    lines: list[str] = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(separator) + " |")
    for s in startups:
        row = [
            str(s.id),
            s.name,
            s.category,
            f"{s.funding_usd:,.2f}",
            str(s.employees),
            str(s.founded_year),
            s.country,
            f"{s.revenue_usd:,.2f}",
            "Yes" if s.is_profitable else "No",
        ]
        lines.append("| " + " | ".join(row) + " |")

    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export(startups: list[Startup], file_path: str | Path) -> None:
    p = Path(file_path)
    match p.suffix.lower():
        case ".csv":
            write_csv(startups, p)
        case ".json":
            write_json(startups, p)
        case ".md":
            write_markdown(startups, p)
        case _:
            raise ValueError(f"Unsupported format: {p.suffix!r}. Use .csv, .json, or .md")
