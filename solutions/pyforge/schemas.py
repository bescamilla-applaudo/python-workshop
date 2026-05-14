from pydantic import BaseModel, Field, field_validator
from datetime import datetime


VALID_CATEGORIES = [
    "fintech", "healthtech", "edtech", "saas", "ecommerce", "ai", "other",
]


class StartupCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    category: str = Field(..., description="Startup category")
    funding_usd: float = Field(..., ge=0)
    employees: int = Field(..., ge=1)
    founded_year: int = Field(..., ge=1900)
    country: str = Field(..., min_length=2, max_length=100)
    revenue_usd: float = Field(0.0, ge=0)
    is_profitable: bool = False

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        v_lower = v.lower().strip()
        if v_lower not in VALID_CATEGORIES:
            raise ValueError(
                f"Category must be one of: {', '.join(VALID_CATEGORIES)}"
            )
        return v_lower

    @field_validator("founded_year")
    @classmethod
    def validate_year(cls, v: int) -> int:
        current_year = datetime.now().year
        if v > current_year:
            raise ValueError(
                f"Founded year cannot be in the future (max: {current_year})"
            )
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty or whitespace")
        return v


class StartupResponse(BaseModel):
    id: int
    name: str
    category: str
    funding_usd: float
    employees: int
    founded_year: int
    country: str
    revenue_usd: float
    is_profitable: bool

    model_config = {"from_attributes": True}


class StartupUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=200)
    category: str | None = None
    funding_usd: float | None = Field(None, ge=0)
    employees: int | None = Field(None, ge=1)
    country: str | None = Field(None, min_length=2, max_length=100)
    revenue_usd: float | None = Field(None, ge=0)
    is_profitable: bool | None = None

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v_lower = v.lower().strip()
        if v_lower not in VALID_CATEGORIES:
            raise ValueError(
                f"Category must be one of: {', '.join(VALID_CATEGORIES)}"
            )
        return v_lower


class StartupFilter(BaseModel):
    category: str | None = None
    min_funding: float | None = Field(None, ge=0)
    max_funding: float | None = None
    min_employees: int | None = Field(None, ge=0)
    country: str | None = None
    is_profitable: bool | None = None
