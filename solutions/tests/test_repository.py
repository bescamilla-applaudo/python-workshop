from pyforge.models import Startup
from pyforge.repository import StartupRepository


def test_add_and_get(repo: StartupRepository):
    startup = repo.get(1)
    assert startup is not None
    assert startup.name == "Alpha"


def test_get_nonexistent(repo: StartupRepository):
    assert repo.get(999) is None


def test_get_all(repo: StartupRepository):
    all_startups = repo.get_all()
    assert len(all_startups) == 5


def test_update(repo: StartupRepository):
    updated = repo.update(1, name="Alpha v2", funding_usd=10_000_000)
    assert updated is not None
    assert updated.name == "Alpha v2"
    assert updated.funding_usd == 10_000_000


def test_update_nonexistent(repo: StartupRepository):
    assert repo.update(999, name="X") is None


def test_delete(repo: StartupRepository):
    assert repo.delete(1) is True
    assert repo.get(1) is None
    assert len(repo) == 4


def test_delete_nonexistent(repo: StartupRepository):
    assert repo.delete(999) is False


def test_search(repo: StartupRepository):
    results = repo.search("alpha")
    assert len(results) == 1
    assert results[0].name == "Alpha"


def test_search_case_insensitive(repo: StartupRepository):
    results = repo.search("BETA")
    assert len(results) == 1
    assert results[0].name == "Beta"


def test_filter_by_category(repo: StartupRepository):
    results = repo.filter_by_category("ai")
    assert len(results) == 1
    assert results[0].name == "Gamma"


def test_filter_by_profitable(repo: StartupRepository):
    results = repo.filter_by_profitable(True)
    assert len(results) == 2


def test_sort_by_funding(repo: StartupRepository):
    sorted_list = repo.sort_by("funding_usd", reverse=True)
    assert sorted_list[0].name == "Gamma"
    assert sorted_list[-1].name == "Delta"


def test_len(repo: StartupRepository):
    assert len(repo) == 5


def test_contains(repo: StartupRepository):
    assert 1 in repo
    assert 999 not in repo


def test_iter(repo: StartupRepository):
    names = [s.name for s in repo]
    assert "Alpha" in names
    assert len(names) == 5
