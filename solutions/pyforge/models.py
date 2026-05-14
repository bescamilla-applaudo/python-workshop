from dataclasses import dataclass
from datetime import datetime


@dataclass
class Startup:
    id: int
    name: str
    category: str
    funding_usd: float
    employees: int
    founded_year: int
    country: str
    revenue_usd: float
    is_profitable: bool

    @property
    def age(self) -> int:
        return datetime.now().year - self.founded_year

    @property
    def funding_per_employee(self) -> float:
        if self.employees <= 0:
            return 0.0
        return self.funding_usd / self.employees

    def __repr__(self) -> str:
        return f"Startup(id={self.id}, name='{self.name}', category='{self.category}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Startup):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class AnalysisResult:
    total_startups: int
    total_funding: float
    avg_funding: float
    avg_employees: int
    categories: dict[str, int]
    profitable_count: int
    profitable_percentage: float
