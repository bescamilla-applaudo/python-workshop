import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

logger = logging.getLogger("pyforge")

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("%s completed in %.4fs", func.__qualname__, elapsed)
        return result
    return wrapper


def log_call(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info("Calling %s | args=%s kwargs=%s", func.__qualname__, args, kwargs)
        try:
            result = func(*args, **kwargs)
            logger.info("%s returned %r", func.__qualname__, result)
            return result
        except Exception as exc:
            logger.error("%s raised %s: %s", func.__qualname__, type(exc).__name__, exc)
            raise
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: Exception
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    logger.warning(
                        "%s attempt %d/%d failed: %s",
                        func.__qualname__, attempt, max_attempts, exc,
                    )
                    if attempt < max_attempts:
                        time.sleep(delay)
            logger.error("%s failed after %d attempts", func.__qualname__, max_attempts)
            raise last_exc
        return wrapper
    return decorator


def validate_non_empty(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        for i, arg in enumerate(args):
            if isinstance(arg, (list, dict, str)) and not arg:
                raise ValueError(
                    f"Argument at position {i} passed to {func.__qualname__} must not be empty"
                )
        for key, val in kwargs.items():
            if isinstance(val, (list, dict, str)) and not val:
                raise ValueError(
                    f"Keyword argument '{key}' passed to {func.__qualname__} must not be empty"
                )
        return func(*args, **kwargs)
    return wrapper
