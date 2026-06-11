from pyforge.models import Startup
from pyforge.analysis import (
    analyze,
    top_funded,
    by_country,
    funding_by_category,
    filter_startups,
)


def test_analyze(sample_startups: list[Startup]):
    result = analyze(sample_startups)
    assert result.total_startups == 5
    assert result.total_funding == 143_000_000
    assert result.profitable_count == 2
    assert result.profitable_percentage == 40.0


def test_analyze_empty():
    result = analyze([])
    assert result.total_startups == 0
    assert result.total_funding == 0.0


def test_top_funded(sample_startups: list[Startup]):
    top = top_funded(sample_startups, 3)
    assert len(top) == 3
    assert top[0].name == "Gamma"
    assert top[1].name == "Beta"


def test_by_country(sample_startups: list[Startup]):
    grouped = by_country(sample_startups)
    assert len(grouped["United States"]) == 2
    assert len(grouped["Germany"]) == 1


def test_funding_by_category(sample_startups: list[Startup]):
    result = funding_by_category(sample_startups)
    assert result["ai"] == 100_000_000
    assert result["fintech"] == 5_000_000


def test_filter_by_category(sample_startups: list[Startup]):
    result = filter_startups(sample_startups, category="ai")
    assert len(result) == 1


def test_filter_by_min_funding(sample_startups: list[Startup]):
    result = filter_startups(sample_startups, min_funding=10_000_000)
    assert len(result) == 3


def test_filter_combined(sample_startups: list[Startup]):
    result = filter_startups(
        sample_startups,
        country="United States",
        is_profitable=True,
    )
    assert len(result) == 1
    assert result[0].name == "Gamma"
