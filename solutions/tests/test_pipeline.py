from pyforge.pipeline import (
    run_pipeline,
    add_funding_tier,
    normalize_country,
)


def test_pipeline_basic():
    data = [
        {
            "name": "TestCo",
            "category": "saas",
            "funding_usd": 1_000_000,
            "employees": 10,
            "founded_year": 2022,
            "country": "US",
            "revenue_usd": 0,
            "is_profitable": False,
        },
    ]
    results = run_pipeline(data)
    assert len(results) == 1
    assert results[0]["name"] == "TestCo"


def test_pipeline_skips_invalid():
    data = [
        {
            "name": "Valid",
            "category": "saas",
            "funding_usd": 100,
            "employees": 10,
            "founded_year": 2022,
            "country": "US",
            "revenue_usd": 0,
            "is_profitable": False,
        },
        {
            "name": "",
            "category": "invalid",
            "funding_usd": -1,
            "employees": 0,
            "founded_year": 2099,
            "country": "",
            "revenue_usd": 0,
            "is_profitable": False,
        },
    ]
    results = run_pipeline(data)
    assert len(results) == 1


def test_pipeline_with_transformations():
    data = [
        {
            "name": "TestCo",
            "category": "saas",
            "funding_usd": 50_000_000,
            "employees": 10,
            "founded_year": 2022,
            "country": "US",
            "revenue_usd": 0,
            "is_profitable": False,
        },
    ]
    results = run_pipeline(
        data, transformations=[add_funding_tier, normalize_country]
    )
    assert results[0]["funding_tier"] == "Series A-B"
    assert results[0]["country"] == "United States"


def test_add_funding_tier():
    assert add_funding_tier({"funding_usd": 200_000_000})["funding_tier"] == "Series C+"
    assert add_funding_tier({"funding_usd": 50_000_000})["funding_tier"] == "Series A-B"
    assert add_funding_tier({"funding_usd": 5_000_000})["funding_tier"] == "Seed"
    assert add_funding_tier({"funding_usd": 500_000})["funding_tier"] == "Pre-seed"


def test_normalize_country():
    assert normalize_country({"country": "US"})["country"] == "United States"
    assert normalize_country({"country": "UK"})["country"] == "United Kingdom"
    assert normalize_country({"country": "Mexico"})["country"] == "Mexico"


def test_pipeline_empty_input():
    results = run_pipeline([])
    assert results == []
