from collections.abc import Callable, Generator

from pydantic import ValidationError

from pyforge.schemas import StartupCreate

_COUNTRY_ALIASES = {
    "US": "United States",
    "UK": "United Kingdom",
}


def read_records(data: list[dict]) -> Generator[dict, None, None]:
    for record in data:
        yield record


def validate_records(records: Generator[dict, None, None]) -> Generator[dict, None, None]:
    for record in records:
        try:
            validated = StartupCreate.model_validate(record)
            yield validated.model_dump()
        except ValidationError as exc:
            print(f"[WARNING] Skipping invalid record {record.get('name', '?')!r}: {exc.error_count()} error(s)")


def transform_records(
    records: Generator[dict, None, None],
    transformations: list[Callable[[dict], dict]] | None = None,
) -> Generator[dict, None, None]:
    if not transformations:
        yield from records
        return
    for record in records:
        for fn in transformations:
            record = fn(record)
        yield record


def collect(records: Generator[dict, None, None]) -> list[dict]:
    return list(records)


def run_pipeline(
    data: list[dict],
    transformations: list[Callable[[dict], dict]] | None = None,
) -> list[dict]:
    records = read_records(data)
    records = validate_records(records)
    records = transform_records(records, transformations)
    return collect(records)


def add_funding_tier(record: dict) -> dict:
    funding = record.get("funding_usd", 0)
    if funding < 500_000:
        tier = "Pre-seed"
    elif funding < 2_000_000:
        tier = "Seed"
    elif funding < 15_000_000:
        tier = "Series A"
    elif funding < 50_000_000:
        tier = "Series B"
    else:
        tier = "Series C+"
    return {**record, "funding_tier": tier}


def normalize_country(record: dict) -> dict:
    country = record.get("country", "")
    return {**record, "country": _COUNTRY_ALIASES.get(country, country)}
