import pytest

from pyforge.analysis import (
    analyze,
    by_country,
    filter_startups,
    funding_by_category,
    top_funded,
)


def test_analyze(sample_startups):
    result = analyze(sample_startups)
    assert result.total_startups == 5
    assert result.total_funding == sum(s.funding_usd for s in sample_startups)
    assert result.avg_funding == result.total_funding / 5
    assert result.profitable_count == 3
    assert abs(result.profitable_percentage - 60.0) < 0.01
    assert set(result.categories.keys()) == {"fintech", "saas", "ai", "edtech", "healthtech"}
    assert result.categories["fintech"] == 1


def test_analyze_avg_employees(sample_startups):
    expected = int(sum(s.employees for s in sample_startups) / len(sample_startups))
    assert analyze(sample_startups).avg_employees == expected


def test_analyze_empty():
    result = analyze([])
    assert result.total_startups == 0
    assert result.total_funding == 0.0
    assert result.avg_funding == 0.0
    assert result.avg_employees == 0
    assert result.categories == {}
    assert result.profitable_count == 0
    assert result.profitable_percentage == 0.0


def test_top_funded_default(sample_startups):
    results = top_funded(sample_startups)
    assert len(results) == 5
    fundings = [s.funding_usd for s in results]
    assert fundings == sorted(fundings, reverse=True)


def test_top_funded_n(sample_startups):
    results = top_funded(sample_startups, n=3)
    assert len(results) == 3
    assert results[0].funding_usd >= results[1].funding_usd >= results[2].funding_usd


def test_top_funded_n_larger_than_list(sample_startups):
    results = top_funded(sample_startups, n=100)
    assert len(results) == len(sample_startups)


def test_by_country(sample_startups):
    grouped = by_country(sample_startups)
    assert "United States" in grouped
    assert len(grouped["United States"]) == 2
    assert "Canada" in grouped
    assert len(grouped["Canada"]) == 1


def test_by_country_all_accounted(sample_startups):
    grouped = by_country(sample_startups)
    total = sum(len(v) for v in grouped.values())
    assert total == len(sample_startups)


def test_funding_by_category(sample_startups):
    result = funding_by_category(sample_startups)
    assert result["fintech"] == 5_000_000.0
    assert result["ai"] == 30_000_000.0
    total = sum(result.values())
    assert abs(total - sum(s.funding_usd for s in sample_startups)) < 0.01


def test_filter_by_category(sample_startups):
    results = filter_startups(sample_startups, category="ai")
    assert len(results) == 1
    assert results[0].name == "NeuralAI Labs"


def test_filter_by_min_funding(sample_startups):
    results = filter_startups(sample_startups, min_funding=10_000_000.0)
    assert all(s.funding_usd >= 10_000_000.0 for s in results)
    assert len(results) == 3


def test_filter_by_max_funding(sample_startups):
    results = filter_startups(sample_startups, max_funding=5_000_000.0)
    assert all(s.funding_usd <= 5_000_000.0 for s in results)


def test_filter_by_country(sample_startups):
    results = filter_startups(sample_startups, country="United States")
    assert len(results) == 2
    assert all(s.country == "United States" for s in results)


def test_filter_by_profitable(sample_startups):
    results = filter_startups(sample_startups, is_profitable=True)
    assert len(results) == 3
    assert all(s.is_profitable for s in results)


def test_filter_combined(sample_startups):
    results = filter_startups(
        sample_startups,
        country="United States",
        is_profitable=True,
        min_funding=1_000_000.0,
    )
    assert len(results) == 1
    assert results[0].name == "Acme Fintech"


def test_filter_no_match(sample_startups):
    results = filter_startups(sample_startups, category="ecommerce")
    assert results == []
