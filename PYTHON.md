# Python: From Zero to AI Engineer
> **Context:** Theoretical reference for those who need to master modern Python for enterprise projects (FastAPI + SQLAlchemy 2.0 + LangGraph + PostgreSQL). No prior Python experience is assumed.
>
> **Documentation source:** Plan built with Context7 from official FastAPI, SQLAlchemy 2.0, Pydantic v2 documentation.
>
> **Methodology:** Don't read first, do first. Each phase ends with a functional mini-project that validates what was learned.

---

## Mental Map: Key Python Concepts

| Concept | What it does |
|---|---|
| `def` / `async def` | Defines synchronous and asynchronous functions |
| `list`, `dict`, `tuple` | Fundamental collections (list, dictionary, immutable tuple) |
| `class` with `__init__` | Class with constructor |
| `pydantic.BaseModel` | Data validation with declarative schema |
| `FastAPI` + `@app.get` | Web framework with typed endpoints |
| `SQLAlchemy AsyncSession` | Async ORM for databases |
| `Depends()` in FastAPI | Dependency injection (DB, auth, etc.) |
| `alembic upgrade head` | Database migrations |
| `venv` | Isolated virtual environment for dependencies |

---

## Phase 1 — Python Core (The Foundation)
**Estimated duration:** 3-5 days
**Goal:** Write Python as if it were your second language.

### Concepts to master

#### 1.1 Data types and control flow
```python
# Basic types — everything is typed from Python 3.10+
name: str = "PyForge"
count: int = 42
price: float = 9.99
active: bool = True
tags: list[str] = ["ai", "fastapi"]
config: dict[str, str] = {"env": "production"}

# Conditional with walrus operator (modern)
if data := get_data():
    print(data)

# Comprehensions (equivalent to .map() and .filter() in JS)
squares = [x ** 2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
lookup = {item["id"]: item for item in items}
```

#### 1.2 Functions and scope
```python
# Type hints (mandatory in professional projects)
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# *args and **kwargs — equivalent to (...args) and {...props}
def log(level: str, *messages: str, **metadata: str) -> None:
    print(f"[{level}]", *messages, metadata)

# Lambda (like arrow functions but limited to a single expression)
double = lambda x: x * 2
```

#### 1.3 Classes and Object-Oriented Programming
```python
from dataclasses import dataclass
from typing import Optional

# Modern form (standard form in modern projects)
@dataclass
class Product:
    id: int
    name: str
    price: float
    description: Optional[str] = None

    def apply_discount(self, percent: float) -> float:
        return self.price * (1 - percent / 100)

# Inheritance
class DigitalProduct(Product):
    download_url: str

    def __repr__(self) -> str:
        return f"DigitalProduct({self.name})"
```

#### 1.4 Error handling
```python
# Python uses try/except, not try/catch
try:
    result = risky_operation()
except ValueError as e:
    print(f"Validation error: {e}")
except (KeyError, IndexError) as e:
    print(f"Data error: {e}")
finally:
    cleanup()

# Custom exceptions — as defined in professional projects
class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        super().__init__(f"Product {product_id} not found")
        self.product_id = product_id
```

#### 1.5 Async / Await — The most critical for backend
```python
import asyncio
from typing import AsyncGenerator

# async def = async function in JS
async def fetch_product(product_id: int) -> dict:
    await asyncio.sleep(1)  # simulates I/O
    return {"id": product_id, "name": "Widget"}

# Async context managers (as used with DB sessions)
async def process():
    async with get_db_session() as session:  # closes automatically
        result = await session.execute(query)

# Async generators (for streaming LLM responses)
async def stream_tokens() -> AsyncGenerator[str, None]:
    for token in ["Hello", " ", "World"]:
        await asyncio.sleep(0.1)
        yield token
```

### Practice 1 — Mini Product CLI
**Objective:** Create a Python script that manages products in memory.

```
python-workshop/
└── phase1/
    ├── models.py       # Product, Category dataclasses
    ├── repository.py   # In-memory list with CRUD
    ├── cli.py          # User input, menu logic
    └── main.py         # Entry point
```

**Success criteria:** The script runs, accepts user input, and handles errors without crashing.

---

## Phase 2 — Pydantic v2 (Declarative Validation)
**Estimated duration:** 2-3 days
**Goal:** Validate and transform data the way professional projects do.

### Why Pydantic is central in modern Python projects
In professional FastAPI projects, **all** request and response bodies are Pydantic classes. FastAPI uses them for automatic validation, serialization, and Swagger generation.

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from decimal import Decimal
from datetime import datetime

# REQUEST schema (what the client sends)
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    description: Optional[str] = Field(None, max_length=1000)
    category_id: int

    # Field validator — transforms or rejects the value before creating the model
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("Name cannot be whitespace")
        return v.strip()

# RESPONSE schema (what the API returns)
class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    created_at: datetime

    # Allows reading from ORM objects directly
    model_config = {"from_attributes": True}
```

### The difference between Model and Schema
```
SQLAlchemy Model  →  Table in the database (app/models/)
Pydantic Schema   →  API JSON contract (app/schemas/)
```

### Practice 2 — E-commerce API Schemas
Create Pydantic schemas for: `UserCreate`, `UserResponse`, `ProductCreate`, `OrderCreate`, `OrderResponse`. Include email validation, positive price, and future dates.

---

## Phase 3 — FastAPI (Modern Web Framework)
**Estimated duration:** 5-7 days
**Goal:** Understand how a professional API is built with FastAPI.

### 3.1 The structure of a professional endpoint
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.product import ProductCreate, ProductResponse
from app.crud.product import create_product, get_product

router = APIRouter(prefix="/products", tags=["products"])

# GET with authentication
@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(
    product_id: int,
    current_user = Depends(get_current_active_user),  # ← Dependency injection
    db: AsyncSession = Depends(get_db),               # ← DB session injected
) -> ProductResponse:
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found"
        )
    return product

# POST — create resource
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create(
    product_in: ProductCreate,                        # ← Request body (Pydantic)
    current_user = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ProductResponse:
    return await create_product(db, product_in)
```

### 3.2 Dependency Injection — The most important concept
```python
# Depends() automatically injects dependencies into each request
# It runs before the endpoint and can perform validations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    # Validates JWT, looks up user in DB, returns the user or raises 401
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    # ... validation logic
    return user

# Can be composed (inject within inject)
async def get_current_active_user(
    auth: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not auth.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return auth
```

### 3.3 Global error handling
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "product_id": exc.product_id}
    )
```

### Practice 3 — Mini Task API
```
fastapi-workshop/
└── phase3/
    ├── main.py
    ├── models/
    │   └── task.py         # SQLAlchemy model
    ├── schemas/
    │   └── task.py         # Pydantic schemas
    ├── crud/
    │   └── task.py         # DB operations
    ├── api/
    │   └── tasks.py        # Router with endpoints
    └── core/
        ├── database.py     # AsyncSession setup
        └── security.py     # Basic JWT
```

**Success criteria:** API running at `localhost:8000` with functional Swagger at `/docs`. Full task CRUD with JWT authentication.

---

## Phase 4 — SQLAlchemy 2.0 Async (The Database)
**Estimated duration:** 4-5 days
**Goal:** Understand how to read and write to PostgreSQL with async SQLAlchemy.

### 4.1 Defining models
```python
from sqlalchemy import String, Integer, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # One-to-many relationship
    orders: Mapped[list["Order"]] = relationship(back_populates="user")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total: Mapped[float] = mapped_column(Numeric(10, 2))

    user: Mapped["User"] = relationship(back_populates="orders")
```

### 4.2 Async queries — What goes in app/crud/
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# SELECT with eager loading (avoid N+1 queries)
async def get_user_with_orders(db: AsyncSession, user_id: int):
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.orders))  # loads orders in a single query
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# INSERT
async def create_user(db: AsyncSession, email: str, hashed_pw: str) -> User:
    user = User(email=email, hashed_password=hashed_pw)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # reloads from DB to get id, created_at
    return user

# UPDATE
async def update_user_email(db: AsyncSession, user_id: int, new_email: str) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        user.email = new_email
        await db.commit()
        await db.refresh(user)
    return user
```

### 4.3 Alembic — Database Migrations
```bash
# Create an automatic migration detecting changes in models.py
alembic revision --autogenerate -m "add orders table"

# Apply pending migrations
alembic upgrade head

# View history
alembic history

# Revert the last migration
alembic downgrade -1
```

### Practice 4 — Extend the Task API with relationships
Add a `Project` model with a one-to-many relationship to `Task`. Create a migration with Alembic. Implement the `GET /projects/{id}/tasks` endpoint.

---

## Phase 5 — Advanced Python for AI Engineers
**Estimated duration:** 5-7 days
**Goal:** Language tools that LangGraph and AI pipelines use extensively.

### 5.1 Decorators (LangGraph uses them everywhere)
```python
from functools import wraps
import time
from typing import Callable, TypeVar, Any

F = TypeVar("F", bound=Callable[..., Any])

# Logging decorator (common pattern in production APIs)
def log_execution(func: F) -> F:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        print(f"Starting {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"Completed {func.__name__} in {elapsed:.3f}s")
            return result
        except Exception as e:
            print(f"Failed {func.__name__}: {e}")
            raise
    return wrapper  # type: ignore

@log_execution
async def process_idea(idea: str) -> dict:
    return {"processed": idea}
```

### 5.2 Context Managers and Generators
```python
from contextlib import asynccontextmanager

# Context manager for DB (standard pattern in FastAPI)
@asynccontextmanager
async def get_db_session(engine):
    async with AsyncSession(engine) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Generator for streaming LLM responses
async def stream_llm_response(prompt: str):
    async for chunk in llm.astream(prompt):
        yield chunk.content
```

### 5.3 TypedDict and Protocol (Advanced typing for LangGraph)
```python
from typing import TypedDict, Annotated
import operator

# LangGraph State — standard pattern in LangGraph
class ProjectState(TypedDict):
    project_id: str
    user_input: str
    # Annotated with operator.add = values accumulate (not replaced)
    messages: Annotated[list[str], operator.add]
    diagrams: dict[str, str]
    current_step: str
    error: str | None

# Protocol — like TypeScript interfaces
from typing import Protocol

class AIServiceProtocol(Protocol):
    async def generate(self, prompt: str) -> str: ...
    async def stream(self, prompt: str): ...
```

### 5.4 Environment, logging, and configuration (standard approach)
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    ai_service_url: str = "http://localhost:8080"
    debug: bool = False

    model_config = {"env_file": ".env", "case_sensitive": False}

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Usage
settings = get_settings()
```

### Practice 5 — Text processing pipeline
Create an async pipeline that:
1. Receives a text
2. Cleans and validates it with Pydantic
3. Processes it in chained steps with logging decorators
4. Returns a typed result with TypedDict

---

## Phase 6 — Testing in Python (pytest)
**Estimated duration:** 3-4 days
**Goal:** Understand how FastAPI APIs are tested with pytest.

### 6.1 Basic pytest
```python
# tests/test_product.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# Fixture — prepares state before each test and cleans up after
@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

@pytest.fixture
async def auth_token(client):
    response = await client.post("/v1/auth/login", data={
        "username": "test@example.com",
        "password": "testpassword"
    })
    return response.json()["access_token"]

# Endpoint test
@pytest.mark.asyncio
async def test_create_product(client, auth_token):
    response = await client.post(
        "/v1/products/",
        json={"name": "Test Product", "price": "9.99", "category_id": 1},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
```

### 6.2 Factories (common pattern in enterprise projects)
```python
import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.models.user import User

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    hashed_password = "$2b$12$hashedpasswordexample"
    is_active = True
```

---

## Phase 7 — The Path to AI Engineer
**Estimated duration:** 7-10 days
**Goal:** Understand and be able to build AI pipelines with LangGraph.

> This phase connects directly to the `langgraph-workshop`. It's the bridge between pure Python and AI engineering.

### What you should understand at this point:
1. **What a directed graph is** and why it's better than a linear chain for AI orchestration.
2. **Why states are TypedDicts** and not mutable objects.
3. **How nodes connect**: each node receives state, modifies it, and returns it.
4. **Why the `checkpointer`** allows resuming a graph where it left off (conversation persistence).

```python
# Graph skeleton — to understand LangGraph's structure
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    input: str
    result: str

def process_node(state: State) -> State:
    return {"result": f"Processed: {state['input']}"}

def validate_node(state: State) -> State:
    if not state["result"]:
        raise ValueError("Empty result")
    return state

# Build the graph
graph = StateGraph(State)
graph.add_node("process", process_node)
graph.add_node("validate", validate_node)
graph.set_entry_point("process")
graph.add_edge("process", "validate")
graph.add_edge("validate", END)

app = graph.compile()
result = app.invoke({"input": "Hello PyForge"})
```

---

## Phase Verification Checklist

### Did I complete Phase 1?
- [ ] I can write typed functions without looking at documentation
- [ ] I understand `async/await` and can distinguish when it's needed
- [ ] I can create classes with `@dataclass` and with traditional `class`
- [ ] My practice 1 script runs without errors

### Did I complete Phase 2?
- [ ] I can create a `BaseModel` with custom validations
- [ ] I understand the difference between Schema and Model
- [ ] I can read Pydantic schemas from any FastAPI project

### Did I complete Phase 3?
- [ ] My Task API has functional Swagger at `/docs`
- [ ] I understand how `Depends()` works and why it replaces middleware
- [ ] I can read any FastAPI endpoint and understand its flow

### Did I complete Phase 4?
- [ ] I created at least one migration with Alembic and applied it
- [ ] I understand the difference between lazy loading and `selectinload`
- [ ] I can do full async CRUD with SQLAlchemy

### Did I complete Phase 5?
- [ ] I can write a functional decorator
- [ ] I understand TypedDict and why LangGraph uses it
- [ ] I can read a LangGraph State and understand what it contains

### Did I complete Phase 6?
- [ ] I can run tests of a FastAPI project with `pytest`
- [ ] I can write a new test for an existing endpoint

### Did I complete Phase 7?
- [ ] I can draw on paper the graph of a LangGraph workflow
- [ ] I can add a new node to the graph without breaking the state

---

## Quick Reference Resources

| I need to understand... | Where to look | What it does |
|---|---|---|
| How models are defined | `app/models/` | Classes that represent DB tables |
| How requests are validated | `app/schemas/` | Pydantic schemas for input/output |
| How queries are made | `app/crud/` | Database operations |
| How routes are protected | `app/core/security.py` | JWT + password hashing |
| How AI is orchestrated | `src/tasks/` (LangGraph) | State graphs with AI nodes |
| How env vars are configured | `app/core/config.py` | Settings with pydantic-settings |

---

> **Rule of this workshop:** When you don't understand something, don't search Google first. Ask Copilot: *"Why is this file structured this way?"*. The answer is usually in the project's context.
