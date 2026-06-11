from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

VALID_CATEGORIES = ["fintech", "healthtech", "edtech", "saas", "ecommerce", "ai", "other"]


class StartupCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    category: str
    funding_usd: float = Field(ge=0)
    employees: int = Field(ge=1)
    founded_year: int = Field(ge=1900)
    country: str = Field(min_length=2, max_length=100)
    revenue_usd: float = Field(default=0.0, ge=0)
    is_profitable: bool = False

    @field_validator("name")
    @classmethod
    def name_not_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be blank or whitespace only")
        return v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        normalized = v.strip().lower()
        if normalized not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of {VALID_CATEGORIES}")
        return normalized

    @field_validator("founded_year")
    @classmethod
    def founded_year_not_future(cls, v: int) -> int:
        if v > date.today().year:
            raise ValueError("founded_year cannot be in the future")
        return v


class StartupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    funding_usd: float
    employees: int
    founded_year: int
    country: str
    revenue_usd: float
    is_profitable: bool


class StartupUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    category: str | None = None
    funding_usd: float | None = Field(default=None, ge=0)
    employees: int | None = Field(default=None, ge=1)
    founded_year: int | None = Field(default=None, ge=1900)
    country: str | None = Field(default=None, min_length=2, max_length=100)
    revenue_usd: float | None = Field(default=None, ge=0)
    is_profitable: bool | None = None

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str | None) -> str | None:
        if v is None:
            return v
        normalized = v.strip().lower()
        if normalized not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of {VALID_CATEGORIES}")
        return normalized


class StartupFilter(BaseModel):
    category: str | None = None
    min_funding: float | None = None
    max_funding: float | None = None
    min_employees: int | None = None
    country: str | None = None
    is_profitable: bool | None = None
