from datetime import date

from pyforge.models import Startup


def make_startup(**overrides) -> Startup:
    defaults = dict(
        id=1, name="Test Co", category="saas", funding_usd=1_000_000.0,
        employees=10, founded_year=2020, country="US", revenue_usd=0.0, is_profitable=False,
    )
    return Startup(**{**defaults, **overrides})


def test_creation(sample_startup):
    assert sample_startup.id == 1
    assert sample_startup.name == "Acme Fintech"
    assert sample_startup.category == "fintech"


def test_age(sample_startup):
    expected = date.today().year - sample_startup.founded_year
    assert sample_startup.age == expected


def test_funding_per_employee(sample_startup):
    assert sample_startup.funding_per_employee == 5_000_000.0 / 50


def test_funding_per_employee_zero_employees():
    s = make_startup(employees=0)
    assert s.funding_per_employee == 0.0


def test_equality_same_id():
    a = make_startup(id=1, name="Alpha")
    b = make_startup(id=1, name="Beta")
    assert a == b


def test_inequality_different_id():
    a = make_startup(id=1)
    b = make_startup(id=2)
    assert a != b


def test_equality_non_startup():
    s = make_startup(id=1)
    assert s.__eq__("not a startup") is NotImplemented


def test_hash_same_id():
    a = make_startup(id=42, name="Alpha")
    b = make_startup(id=42, name="Beta")
    assert hash(a) == hash(b)


def test_hash_usable_in_set():
    a = make_startup(id=1)
    b = make_startup(id=1)
    c = make_startup(id=2)
    assert len({a, b, c}) == 2


def test_repr(sample_startup):
    r = repr(sample_startup)
    assert "id=1" in r
    assert "Acme Fintech" in r
    assert "fintech" in r
    assert r.startswith("Startup(")
