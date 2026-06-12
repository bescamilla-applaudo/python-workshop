from datetime import date

import pytest
from pydantic import ValidationError

from pyforge.schemas import StartupCreate, StartupFilter, StartupUpdate

VALID = dict(
    name="Test Startup",
    category="fintech",
    funding_usd=1_000_000.0,
    employees=10,
    founded_year=2015,
    country="US",
    revenue_usd=500_000.0,
    is_profitable=True,
)


def test_valid_creation():
    s = StartupCreate(**VALID)
    assert s.name == "Test Startup"
    assert s.category == "fintech"


def test_category_normalized_to_lowercase():
    s = StartupCreate(**{**VALID, "category": "FinTech"})
    assert s.category == "fintech"


def test_invalid_category():
    with pytest.raises(ValidationError, match="category"):
        StartupCreate(**{**VALID, "category": "blockchain"})


def test_negative_funding():
    with pytest.raises(ValidationError):
        StartupCreate(**{**VALID, "funding_usd": -1.0})


def test_future_founded_year():
    with pytest.raises(ValidationError, match="future"):
        StartupCreate(**{**VALID, "founded_year": date.today().year + 1})


def test_empty_name():
    with pytest.raises(ValidationError):
        StartupCreate(**{**VALID, "name": "   "})


def test_short_name():
    with pytest.raises(ValidationError):
        StartupCreate(**{**VALID, "name": "X"})


def test_zero_employees():
    with pytest.raises(ValidationError):
        StartupCreate(**{**VALID, "employees": 0})


def test_defaults():
    s = StartupCreate(**{k: v for k, v in VALID.items() if k not in ("revenue_usd", "is_profitable")})
    assert s.revenue_usd == 0.0
    assert s.is_profitable is False


def test_partial_update_valid():
    u = StartupUpdate(name="New Name", category="saas")
    assert u.name == "New Name"
    assert u.category == "saas"


def test_partial_update_all_none():
    u = StartupUpdate()
    assert u.name is None
    assert u.category is None


def test_partial_update_invalid_category():
    with pytest.raises(ValidationError):
        StartupUpdate(category="notreal")


def test_partial_update_category_normalized():
    u = StartupUpdate(category="AI")
    assert u.category == "ai"


def test_filter_all_optional():
    f = StartupFilter()
    assert f.category is None
    assert f.min_funding is None
    assert f.is_profitable is None


def test_filter_with_values():
    f = StartupFilter(category="saas", min_funding=1000.0, is_profitable=True)
    assert f.category == "saas"
    assert f.min_funding == 1000.0
    assert f.is_profitable is True
