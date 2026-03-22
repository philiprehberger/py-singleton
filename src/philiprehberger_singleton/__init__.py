"""Thread-safe singleton and multiton pattern decorators."""

from __future__ import annotations

import inspect
import threading
from typing import Any, TypeVar

__all__ = ["multiton", "singleton"]

T = TypeVar("T")


def singleton(cls: type[T]) -> type[T]:
    """Decorator that makes a class a thread-safe singleton.

    The decorated class will return the same instance on every instantiation.
    Call ``cls.reset()`` to discard the cached instance.

    Args:
        cls: The class to decorate.

    Returns:
        The decorated class with singleton behaviour.
    """
    lock = threading.Lock()
    instance_holder: dict[str, T | None] = {"instance": None}
    original_init = cls.__init__

    def __new__(mcs: type[T], *args: Any, **kwargs: Any) -> T:  # noqa: ARG001
        with lock:
            if instance_holder["instance"] is None:
                obj = object.__new__(mcs)
                instance_holder["instance"] = obj
                original_init(obj, *args, **kwargs)
            return instance_holder["instance"]  # type: ignore[return-value]

    def __init__(self: Any, *args: Any, **kwargs: Any) -> None:  # noqa: ARG001
        pass  # init is called in __new__

    @staticmethod
    def reset() -> None:
        """Discard the cached singleton instance."""
        with lock:
            instance_holder["instance"] = None

    cls.__new__ = __new__  # type: ignore[assignment]
    cls.__init__ = __init__  # type: ignore[assignment]
    cls.reset = reset  # type: ignore[attr-defined]
    return cls


def multiton(key: str) -> Any:
    """Decorator factory that makes a class a thread-safe multiton.

    One instance is cached per unique value of the constructor argument
    identified by *key*.

    Call ``cls.reset()`` to discard **all** cached instances.

    Args:
        key: The name of the ``__init__`` parameter used as instance key.

    Returns:
        A class decorator.
    """

    def decorator(cls: type[T]) -> type[T]:
        lock = threading.Lock()
        instances: dict[Any, T] = {}
        original_init = cls.__init__
        sig = inspect.signature(original_init)
        params = [p for p in sig.parameters if p != "self"]

        def __new__(mcs: type[T], *args: Any, **kwargs: Any) -> T:
            key_value: Any = None
            if key in kwargs:
                key_value = kwargs[key]
            else:
                try:
                    idx = params.index(key)
                    if idx < len(args):
                        key_value = args[idx]
                except (ValueError, IndexError):
                    pass

            with lock:
                if key_value not in instances:
                    obj = object.__new__(mcs)
                    original_init(obj, *args, **kwargs)
                    instances[key_value] = obj
                return instances[key_value]

        def __init__(self: Any, *args: Any, **kwargs: Any) -> None:  # noqa: ARG001
            pass  # init is called in __new__

        @staticmethod
        def reset() -> None:
            """Discard all cached multiton instances."""
            with lock:
                instances.clear()

        cls.__new__ = __new__  # type: ignore[assignment]
        cls.__init__ = __init__  # type: ignore[assignment]
        cls.reset = reset  # type: ignore[attr-defined]
        return cls

    return decorator
