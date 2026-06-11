from pyforge.models import AnalysisResult, Startup


def analyze(startups: list[Startup]) -> AnalysisResult:
    total = len(startups)
    total_funding = sum(s.funding_usd for s in startups)
    avg_funding = total_funding / total if total else 0.0
    avg_employees = int(sum(s.employees for s in startups) / total) if total else 0

    categories: dict[str, int] = {}
    for s in startups:
        categories[s.category] = categories.get(s.category, 0) + 1

    profitable_count = sum(1 for s in startups if s.is_profitable)
    profitable_percentage = (profitable_count / total * 100) if total else 0.0

    return AnalysisResult(
        total_startups=total,
        total_funding=total_funding,
        avg_funding=avg_funding,
        avg_employees=avg_employees,
        categories=categories,
        profitable_count=profitable_count,
        profitable_percentage=profitable_percentage,
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
    if category is not None:
        result = [s for s in result if s.category == category]
    if min_funding is not None:
        result = [s for s in result if s.funding_usd >= min_funding]
    if max_funding is not None:
        result = [s for s in result if s.funding_usd <= max_funding]
    if min_employees is not None:
        result = [s for s in result if s.employees >= min_employees]
    if country is not None:
        result = [s for s in result if s.country == country]
    if is_profitable is not None:
        result = [s for s in result if s.is_profitable == is_profitable]
    return result
