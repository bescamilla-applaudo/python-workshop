from typing import Generator, Callable

from .schemas import StartupCreate


def read_records(data: list[dict]) -> Generator[dict, None, None]:
    for record in data:
        yield record


def validate_records(
    records: Generator[dict, None, None],
) -> Generator[dict, None, None]:
    for record in records:
        try:
            validated = StartupCreate(**record)
            yield validated.model_dump()
        except Exception as e:
            print(f"  Warning: Skipping invalid record: {e}")


def transform_records(
    records: Generator[dict, None, None],
    transformations: list[Callable[[dict], dict]] | None = None,
) -> Generator[dict, None, None]:
    for record in records:
        if transformations:
            for transform in transformations:
                record = transform(record)
        yield record


def collect(records: Generator[dict, None, None]) -> list[dict]:
    return list(records)


def run_pipeline(
    data: list[dict],
    transformations: list[Callable[[dict], dict]] | None = None,
) -> list[dict]:
    step1 = read_records(data)
    step2 = validate_records(step1)
    step3 = transform_records(step2, transformations)
    return collect(step3)


# --- Transformation functions ---


def add_funding_tier(record: dict) -> dict:
    funding = record.get("funding_usd", 0)
    if funding >= 100_000_000:
        record["funding_tier"] = "Series C+"
    elif funding >= 10_000_000:
        record["funding_tier"] = "Series A-B"
    elif funding >= 1_000_000:
        record["funding_tier"] = "Seed"
    else:
        record["funding_tier"] = "Pre-seed"
    return record


def normalize_country(record: dict) -> dict:
    country_map = {
        "US": "United States",
        "USA": "United States",
        "UK": "United Kingdom",
        "GB": "United Kingdom",
    }
    country = record.get("country", "")
    record["country"] = country_map.get(country.upper(), country)
    return record
