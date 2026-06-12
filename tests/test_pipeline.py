import pytest

from pyforge.pipeline import (
    add_funding_tier,
    collect,
    normalize_country,
    read_records,
    run_pipeline,
    transform_records,
    validate_records,
)

VALID_RECORD = dict(
    name="Pipeline Co",
    category="saas",
    funding_usd=1_000_000.0,
    employees=10,
    founded_year=2018,
    country="US",
    revenue_usd=500_000.0,
    is_profitable=False,
)


def test_read_records_yields_all():
    data = [{"a": 1}, {"a": 2}, {"a": 3}]
    assert list(read_records(data)) == data


def test_validate_records_passes_valid():
    records = read_records([VALID_RECORD])
    result = collect(validate_records(records))
    assert len(result) == 1
    assert result[0]["name"] == "Pipeline Co"


def test_validate_records_skips_invalid(capsys):
    invalid = {**VALID_RECORD, "employees": -5}
    records = read_records([VALID_RECORD, invalid])
    result = collect(validate_records(records))
    assert len(result) == 1
    captured = capsys.readouterr()
    assert "[WARNING]" in captured.out


def test_validate_records_skips_multiple_invalid(capsys):
    bad1 = {**VALID_RECORD, "employees": 0}
    bad2 = {**VALID_RECORD, "funding_usd": -100}
    records = read_records([bad1, bad2, VALID_RECORD])
    result = collect(validate_records(records))
    assert len(result) == 1


def test_transform_records_no_transformations():
    records = read_records([VALID_RECORD])
    validated = validate_records(records)
    result = collect(transform_records(validated, None))
    assert len(result) == 1


def test_transform_records_applies_all():
    def add_flag(r):
        return {**r, "flagged": True}

    def add_score(r):
        return {**r, "score": 99}

    records = read_records([VALID_RECORD])
    validated = validate_records(records)
    result = collect(transform_records(validated, [add_flag, add_score]))
    assert result[0]["flagged"] is True
    assert result[0]["score"] == 99


def test_run_pipeline_basic():
    result = run_pipeline([VALID_RECORD])
    assert len(result) == 1
    assert result[0]["name"] == "Pipeline Co"


def test_run_pipeline_with_transformations():
    result = run_pipeline([VALID_RECORD], transformations=[add_funding_tier])
    assert "funding_tier" in result[0]


def test_run_pipeline_empty_input():
    result = run_pipeline([])
    assert result == []


def test_run_pipeline_filters_invalid(capsys):
    bad = {**VALID_RECORD, "category": "notacategory"}
    result = run_pipeline([VALID_RECORD, bad])
    assert len(result) == 1


# add_funding_tier tiers

def test_funding_tier_pre_seed():
    r = {**VALID_RECORD, "funding_usd": 100_000.0}
    assert add_funding_tier(r)["funding_tier"] == "Pre-seed"


def test_funding_tier_seed():
    r = {**VALID_RECORD, "funding_usd": 1_000_000.0}
    assert add_funding_tier(r)["funding_tier"] == "Seed"


def test_funding_tier_series_a():
    r = {**VALID_RECORD, "funding_usd": 5_000_000.0}
    assert add_funding_tier(r)["funding_tier"] == "Series A"


def test_funding_tier_series_b():
    r = {**VALID_RECORD, "funding_usd": 20_000_000.0}
    assert add_funding_tier(r)["funding_tier"] == "Series B"


def test_funding_tier_series_c_plus():
    r = {**VALID_RECORD, "funding_usd": 100_000_000.0}
    assert add_funding_tier(r)["funding_tier"] == "Series C+"


def test_funding_tier_boundary_seed():
    r = {**VALID_RECORD, "funding_usd": 500_000.0}
    assert add_funding_tier(r)["funding_tier"] == "Seed"


def test_funding_tier_does_not_mutate():
    r = {**VALID_RECORD, "funding_usd": 1_000_000.0}
    original = dict(r)
    add_funding_tier(r)
    assert r == original


# normalize_country

def test_normalize_us():
    r = {**VALID_RECORD, "country": "US"}
    assert normalize_country(r)["country"] == "United States"


def test_normalize_uk():
    r = {**VALID_RECORD, "country": "UK"}
    assert normalize_country(r)["country"] == "United Kingdom"


def test_normalize_unknown_country():
    r = {**VALID_RECORD, "country": "Germany"}
    assert normalize_country(r)["country"] == "Germany"


def test_normalize_does_not_mutate():
    r = {**VALID_RECORD, "country": "US"}
    original = dict(r)
    normalize_country(r)
    assert r == original
