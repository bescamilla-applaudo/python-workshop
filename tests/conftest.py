import pytest

from pyforge.models import Startup
from pyforge.repository import StartupRepository


@pytest.fixture
def sample_startup() -> Startup:
    return Startup(
        id=1,
        name="Acme Fintech",
        category="fintech",
        funding_usd=5_000_000.0,
        employees=50,
        founded_year=2018,
        country="United States",
        revenue_usd=1_200_000.0,
        is_profitable=True,
    )


@pytest.fixture
def sample_startups() -> list[Startup]:
    return [
        Startup(
            id=1,
            name="Acme Fintech",
            category="fintech",
            funding_usd=5_000_000.0,
            employees=50,
            founded_year=2018,
            country="United States",
            revenue_usd=1_200_000.0,
            is_profitable=True,
        ),
        Startup(
            id=2,
            name="CloudSaaS Pro",
            category="saas",
            funding_usd=12_000_000.0,
            employees=120,
            founded_year=2016,
            country="United Kingdom",
            revenue_usd=4_500_000.0,
            is_profitable=True,
        ),
        Startup(
            id=3,
            name="NeuralAI Labs",
            category="ai",
            funding_usd=30_000_000.0,
            employees=200,
            founded_year=2020,
            country="United States",
            revenue_usd=500_000.0,
            is_profitable=False,
        ),
        Startup(
            id=4,
            name="LearnEdge",
            category="edtech",
            funding_usd=800_000.0,
            employees=15,
            founded_year=2021,
            country="Canada",
            revenue_usd=150_000.0,
            is_profitable=False,
        ),
        Startup(
            id=5,
            name="MediTrack",
            category="healthtech",
            funding_usd=20_000_000.0,
            employees=90,
            founded_year=2017,
            country="Germany",
            revenue_usd=8_000_000.0,
            is_profitable=True,
        ),
    ]


@pytest.fixture
def repo(sample_startups: list[Startup]) -> StartupRepository:
    r = StartupRepository()
    for s in sample_startups:
        r.add(s)
    return r
