from collections import Counter

from .models import Startup, AnalysisResult


def analyze(startups: list[Startup]) -> AnalysisResult:
    if not startups:
        return AnalysisResult(
            total_startups=0,
            total_funding=0.0,
            avg_funding=0.0,
            avg_employees=0,
            categories={},
            profitable_count=0,
            profitable_percentage=0.0,
        )

    total_funding = sum(s.funding_usd for s in startups)
    profitable = [s for s in startups if s.is_profitable]
    categories = dict(Counter(s.category for s in startups))

    return AnalysisResult(
        total_startups=len(startups),
        total_funding=total_funding,
        avg_funding=total_funding / len(startups),
        avg_employees=sum(s.employees for s in startups) // len(startups),
        categories=categories,
        profitable_count=len(profitable),
        profitable_percentage=len(profitable) / len(startups) * 100,
    )


def top_funded(startups: list[Startup], n: int = 5) -> list[Startup]:
    return sorted(startups, key=lambda s: s.funding_usd, reverse=True)[:n]


def by_country(startups: list[Startup]) -> dict[str, list[Startup]]:
    result: dict[str, list[Startup]] = {}
    for s in startups:
        result.setdefault(s.country, []).append(s)
    return result


def funding_by_category(startups: list[Startup]) -> dict[str, float]:
    result: dict[str, float] = {}
    for s in startups:
        result[s.category] = result.get(s.category, 0.0) + s.funding_usd
    return result


def filter_startups(
    startups: list[Startup],
    category: str | None = None,
    min_funding: float | None = None,
    max_funding: float | None = None,
    min_employees: int | None = None,
    country: str | None = None,
    is_profitable: bool | None = None,
) -> list[Startup]:
    result = startups
    if category:
        result = [s for s in result if s.category == category]
    if min_funding is not None:
        result = [s for s in result if s.funding_usd >= min_funding]
    if max_funding is not None:
        result = [s for s in result if s.funding_usd <= max_funding]
    if min_employees is not None:
        result = [s for s in result if s.employees >= min_employees]
    if country:
        result = [s for s in result if s.country.lower() == country.lower()]
    if is_profitable is not None:
        result = [s for s in result if s.is_profitable == is_profitable]
    return result
