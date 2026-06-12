import pytest

from pyforge.models import Startup
from pyforge.repository import StartupRepository


def make_startup(id=0, name="Test Co", category="saas", **overrides) -> Startup:
    defaults = dict(
        id=id, name=name, category=category, funding_usd=1_000_000.0,
        employees=10, founded_year=2020, country="US", revenue_usd=0.0, is_profitable=False,
    )
    return Startup(**{**defaults, **overrides})


def test_add_and_get(repo, sample_startup):
    result = repo.get(1)
    assert result is not None
    assert result.name == sample_startup.name


def test_add_auto_id():
    r = StartupRepository()
    s = r.add(make_startup(id=0, name="Auto"))
    assert s.id == 1
    s2 = r.add(make_startup(id=0, name="Auto2"))
    assert s2.id == 2


def test_add_explicit_id():
    r = StartupRepository()
    s = r.add(make_startup(id=99, name="Explicit"))
    assert s.id == 99


def test_get_nonexistent(repo):
    assert repo.get(999) is None


def test_get_all_returns_all(repo, sample_startups):
    assert len(repo.get_all()) == len(sample_startups)


def test_update(repo):
    updated = repo.update(1, name="Updated Name", employees=200)
    assert updated is not None
    assert updated.name == "Updated Name"
    assert updated.employees == 200
    assert repo.get(1).name == "Updated Name"


def test_update_nonexistent(repo):
    assert repo.update(999, name="Ghost") is None


def test_delete(repo):
    assert repo.delete(1) is True
    assert repo.get(1) is None


def test_delete_nonexistent(repo):
    assert repo.delete(999) is False


def test_search_by_name(repo):
    results = repo.search("fintech")
    assert any(s.name == "Acme Fintech" for s in results)


def test_search_case_insensitive(repo):
    results = repo.search("ACME")
    assert len(results) == 1
    assert results[0].name == "Acme Fintech"


def test_search_no_match(repo):
    assert repo.search("xyznotfound") == []


def test_filter_by_category(repo):
    results = repo.filter_by_category("fintech")
    assert all(s.category == "fintech" for s in results)
    assert len(results) == 1


def test_filter_by_profitable_true(repo):
    results = repo.filter_by_profitable(True)
    assert all(s.is_profitable for s in results)
    assert len(results) == 3


def test_filter_by_profitable_false(repo):
    results = repo.filter_by_profitable(False)
    assert all(not s.is_profitable for s in results)
    assert len(results) == 2


def test_sort_by_funding(repo):
    results = repo.sort_by("funding_usd")
    fundings = [s.funding_usd for s in results]
    assert fundings == sorted(fundings)


def test_sort_by_funding_reverse(repo):
    results = repo.sort_by("funding_usd", reverse=True)
    fundings = [s.funding_usd for s in results]
    assert fundings == sorted(fundings, reverse=True)


def test_sort_by_name(repo):
    results = repo.sort_by("name")
    names = [s.name for s in results]
    assert names == sorted(names)


def test_sort_by_computed_property(repo):
    results = repo.sort_by("age", reverse=True)
    ages = [s.age for s in results]
    assert ages == sorted(ages, reverse=True)


def test_len(repo, sample_startups):
    assert len(repo) == len(sample_startups)


def test_contains_existing(repo):
    assert 1 in repo


def test_contains_missing(repo):
    assert 999 not in repo


def test_iter(repo, sample_startups):
    ids = {s.id for s in repo}
    expected = {s.id for s in sample_startups}
    assert ids == expected
