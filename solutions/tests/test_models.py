from datetime import datetime

from pyforge.models import Startup


def test_startup_creation(sample_startup: Startup):
    assert sample_startup.name == "TestStartup"
    assert sample_startup.category == "saas"
    assert sample_startup.funding_usd == 1_000_000


def test_startup_age(sample_startup: Startup):
    expected_age = datetime.now().year - sample_startup.founded_year
    assert sample_startup.age == expected_age


def test_startup_funding_per_employee(sample_startup: Startup):
    assert sample_startup.funding_per_employee == 100_000


def test_startup_funding_per_employee_zero_employees():
    startup = Startup(1, "Test", "saas", 1_000_000, 0, 2022, "US", 0, False)
    assert startup.funding_per_employee == 0.0


def test_startup_equality():
    s1 = Startup(1, "A", "saas", 100, 10, 2020, "US", 0, False)
    s2 = Startup(1, "B", "ai", 200, 20, 2019, "UK", 0, True)
    assert s1 == s2  # same id


def test_startup_inequality():
    s1 = Startup(1, "A", "saas", 100, 10, 2020, "US", 0, False)
    s2 = Startup(2, "A", "saas", 100, 10, 2020, "US", 0, False)
    assert s1 != s2


def test_startup_hash():
    s1 = Startup(1, "A", "saas", 100, 10, 2020, "US", 0, False)
    s2 = Startup(1, "B", "ai", 200, 20, 2019, "UK", 0, True)
    assert hash(s1) == hash(s2)
    assert len({s1, s2}) == 1


def test_startup_repr(sample_startup: Startup):
    assert "TestStartup" in repr(sample_startup)
    assert "saas" in repr(sample_startup)
