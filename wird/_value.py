from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Concatenate, Type, overload

from . import _future as f

__all__ = ("Value",)


@dataclass(slots=True, frozen=True)
class Value[T]:
    internal: T

    @overload
    def unwrap(self) -> T:
        """Returns the container value."""
        ...

    @overload
    def unwrap[R](self, *, as_type: Type[R]) -> R:
        """Returns the contained value casted to passed type.

        No actual casting is performed, type change affects only type checkers.
        """
        ...

    def unwrap(self, **_) -> Any:
        return self.internal

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Value[R]:
        """Maps a Value[T] to Value[R] by applying a function to a contained value."""
        return Value(fn(self.internal, *args, **kwargs))

    def inspect[**P](
        self,
        fn: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Value[T]:
        """Calls a function with a reference to the contained value.

        Returns the original Value.
        """
        fn(self.internal, *args, **kwargs)
        return self

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[R]:
        """Maps a Value[T] to Future[R] by applying a async function to a contained
        value."""

        return f.Future(fn(self.internal, *args, **kwargs))

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[T]:
        """Calls an async function with a reference to the contained value.

        Returns the original value in Future container.
        """
        return f.Future(_inspect_async(self.internal, fn, *args, **kwargs))


async def _inspect_async[T, **P](
    value: T,
    fn: Callable[Concatenate[T, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    await fn(value, *args, **kwargs)
    return value
