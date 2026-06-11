import pytest
from pydantic import ValidationError

from pyforge.schemas import StartupCreate, StartupUpdate, StartupFilter


def test_valid_startup_create():
    s = StartupCreate(
        name="TestCo",
        category="fintech",
        funding_usd=1_000_000,
        employees=10,
        founded_year=2022,
        country="US",
    )
    assert s.name == "TestCo"
    assert s.category == "fintech"


def test_category_normalized_to_lowercase():
    s = StartupCreate(
        name="TestCo",
        category="FINTECH",
        funding_usd=100,
        employees=10,
        founded_year=2022,
        country="US",
    )
    assert s.category == "fintech"


def test_invalid_category():
    with pytest.raises(ValidationError, match="Category must be one of"):
        StartupCreate(
            name="TestCo",
            category="invalid",
            funding_usd=1_000_000,
            employees=10,
            founded_year=2022,
            country="US",
        )


def test_negative_funding():
    with pytest.raises(ValidationError):
        StartupCreate(
            name="TestCo",
            category="saas",
            funding_usd=-100,
            employees=10,
            founded_year=2022,
            country="US",
        )


def test_future_year():
    with pytest.raises(ValidationError, match="cannot be in the future"):
        StartupCreate(
            name="TestCo",
            category="saas",
            funding_usd=100,
            employees=10,
            founded_year=2099,
            country="US",
        )


def test_empty_name():
    with pytest.raises(ValidationError):
        StartupCreate(
            name="   ",
            category="saas",
            funding_usd=100,
            employees=10,
            founded_year=2022,
            country="US",
        )


def test_zero_employees():
    with pytest.raises(ValidationError):
        StartupCreate(
            name="TestCo",
            category="saas",
            funding_usd=100,
            employees=0,
            founded_year=2022,
            country="US",
        )


def test_startup_update_partial():
    u = StartupUpdate(name="New Name")
    assert u.name == "New Name"
    assert u.category is None
    assert u.funding_usd is None


def test_startup_filter():
    f = StartupFilter(category="ai", min_funding=1_000_000)
    assert f.category == "ai"
    assert f.min_funding == 1_000_000
    assert f.country is None
