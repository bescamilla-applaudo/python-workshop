from .models import Startup


class StartupRepository:
    def __init__(self) -> None:
        self._startups: dict[int, Startup] = {}
        self._next_id: int = 1

    def add(self, startup: Startup) -> Startup:
        if startup.id == 0:
            startup.id = self._next_id
            self._next_id += 1
        else:
            self._next_id = max(self._next_id, startup.id + 1)
        self._startups[startup.id] = startup
        return startup

    def get(self, startup_id: int) -> Startup | None:
        return self._startups.get(startup_id)

    def get_all(self) -> list[Startup]:
        return list(self._startups.values())

    def update(self, startup_id: int, **kwargs: object) -> Startup | None:
        startup = self._startups.get(startup_id)
        if startup is None:
            return None
        for key, value in kwargs.items():
            if hasattr(startup, key):
                setattr(startup, key, value)
        return startup

    def delete(self, startup_id: int) -> bool:
        return self._startups.pop(startup_id, None) is not None

    def search(self, query: str) -> list[Startup]:
        query_lower = query.lower()
        return [s for s in self._startups.values() if query_lower in s.name.lower()]

    def filter_by_category(self, category: str) -> list[Startup]:
        return [s for s in self._startups.values() if s.category == category]

    def filter_by_profitable(self, profitable: bool = True) -> list[Startup]:
        return [s for s in self._startups.values() if s.is_profitable == profitable]

    def sort_by(self, field: str, reverse: bool = False) -> list[Startup]:
        return sorted(
            self._startups.values(),
            key=lambda s: getattr(s, field),
            reverse=reverse,
        )

    def __len__(self) -> int:
        return len(self._startups)

    def __contains__(self, startup_id: int) -> bool:
        return startup_id in self._startups

    def __iter__(self):
        return iter(self._startups.values())
