import pytest

from pyforge.models import Startup
from pyforge.repository import StartupRepository


@pytest.fixture
def sample_startup() -> Startup:
    return Startup(
        id=1,
        name="TestStartup",
        category="saas",
        funding_usd=1_000_000,
        employees=10,
        founded_year=2022,
        country="United States",
        revenue_usd=100_000,
        is_profitable=False,
    )


@pytest.fixture
def sample_startups() -> list[Startup]:
    return [
        Startup(1, "Alpha", "fintech", 5_000_000, 50, 2020, "United States", 1_000_000, False),
        Startup(2, "Beta", "saas", 20_000_000, 200, 2018, "Germany", 8_000_000, True),
        Startup(3, "Gamma", "ai", 100_000_000, 500, 2019, "United States", 40_000_000, True),
        Startup(4, "Delta", "edtech", 3_000_000, 30, 2021, "Mexico", 500_000, False),
        Startup(5, "Epsilon", "healthtech", 15_000_000, 120, 2020, "Brazil", 4_000_000, False),
    ]


@pytest.fixture
def repo(sample_startups: list[Startup]) -> StartupRepository:
    repository = StartupRepository()
    for s in sample_startups:
        repository.add(s)
    return repository
