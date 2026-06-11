from typing import Iterator

from pyforge.models import Startup


class StartupRepository:
    def __init__(self) -> None:
        self._data: dict[int, Startup] = {}
        self._next_id: int = 1

    def add(self, startup: Startup) -> Startup:
        if startup.id == 0:
            startup = Startup(
                id=self._next_id,
                name=startup.name,
                category=startup.category,
                funding_usd=startup.funding_usd,
                employees=startup.employees,
                founded_year=startup.founded_year,
                country=startup.country,
                revenue_usd=startup.revenue_usd,
                is_profitable=startup.is_profitable,
            )
            self._next_id += 1
        self._data[startup.id] = startup
        return startup

    def get(self, startup_id: int) -> Startup | None:
        return self._data.get(startup_id)

    def get_all(self) -> list[Startup]:
        return list(self._data.values())

    def update(self, startup_id: int, **kwargs) -> Startup | None:
        startup = self._data.get(startup_id)
        if startup is None:
            return None
        for field, value in kwargs.items():
            setattr(startup, field, value)
        return startup

    def delete(self, startup_id: int) -> bool:
        if startup_id not in self._data:
            return False
        del self._data[startup_id]
        return True

    def search(self, query: str) -> list[Startup]:
        q = query.lower()
        return [s for s in self._data.values() if q in s.name.lower()]

    def filter_by_category(self, category: str) -> list[Startup]:
        return [s for s in self._data.values() if s.category == category]

    def filter_by_profitable(self, profitable: bool = True) -> list[Startup]:
        return [s for s in self._data.values() if s.is_profitable == profitable]

    def sort_by(self, field: str, reverse: bool = False) -> list[Startup]:
        return sorted(self._data.values(), key=lambda s: getattr(s, field), reverse=reverse)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, startup_id: object) -> bool:
        return startup_id in self._data

    def __iter__(self) -> Iterator[Startup]:
        return iter(self._data.values())
