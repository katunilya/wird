from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    Concatenate,
    NoReturn,
    Protocol,
    Type,
    overload,
)

from . import _future as f, maybe

__all__ = (
    "EmptyUnwrapError",
    "Maybe",
    "Some",
    "Empty",
    "FutureMaybe",
)


class EmptyUnwrapError(ValueError):
    """Exception raised on attempt to unwrap Empty container."""


class Maybe[T](Protocol):  # pragma: no cover
    @overload
    def unwrap(self, *, on_empty: str = "expected Some, got Empty") -> T:
        """Returns the contained Some value.

        Because this function may raise EmptyUnwrapError, its use is generally
        discouraged.

        Instead, prefer to use pattern matching and handle the Empty case explicitly, or
        call unwrap_or, unwrap_or_else.
        """
        ...

    @overload
    def unwrap[R](
        self,
        *,
        as_type: Type[R],
        on_empty: str = "expected Some, got Empty",
    ) -> R:
        """Returns the contained Some value casted to passed type.

        Because this function may raise EmptyUnwrapError, its use is generally
        discouraged.

        Instead, prefer to use pattern matching and handle the Empty case explicitly, or
        call unwrap_or, unwrap_or_else.

        No actual casting is performed, type change affects only type checkers.
        """
        ...

    def unwrap_or(self, /, default: T) -> T:
        """Returns the contained Some value or a provided default.

        Arguments passed to unwrap_or are eagerly evaluated; if you are passing the
        result of a function call, it is recommended to use unwrap_or_else, which is
        lazily evaluated.
        """
        ...

    def unwrap_or_none(self) -> T | None:
        """Returns the contained Some value or None."""
        ...

    def unwrap_or_else[**P](
        self,
        fn: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        """Returns the contained Some value or computes it from a sync closure."""
        ...

    def unwrap_or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[T]:
        """Returns the contained Some value or computes it from a async closure."""
        ...

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[R]:
        """Maps a Maybe[T] to Maybe[R] by applying a function to a contained value (if
        Some) or returns Empty (if Empty)."""
        ...

    def inspect[**P](
        self,
        fn: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[T]:
        """Calls a function with a reference to the contained value if Some.

        Returns the original Maybe.
        """
        ...

    def is_some(self) -> bool:
        """Returns true if the Maybe is a Some value."""
        ...

    def is_empty(self) -> bool:
        """Returns true if the Maybe is a Empty value."""
        ...

    def is_some_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        """Returns true if the Maybe is a Some and the value inside of it matches a
        predicate."""
        ...

    def is_empty_or[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        """Returns true if the Maybe is a Empty or the value inside of it matches a
        predicate."""
        ...

    def and_[R](self, other: Maybe[R]) -> Maybe[R]:
        """Returns Empty if the Maybe is Empty, otherwise returns other.

        Arguments passed to and_ are eagerly evaluated; if you are passing the result of
        a function call, it is recommended to use and_then, which is lazily evaluated.
        """
        ...

    def or_(self, other: Maybe[T]) -> Maybe[T]:
        """Returns the Maybe if it contains a value, otherwise returns other.

        Arguments passed to or_ are eagerly evaluated; if you are passing the result of
        a function call, it is recommended to use or_else, which is lazily evaluated.
        """
        ...

    def and_then[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Maybe[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[R]:
        """Returns Empty if the Maybe is Empty, otherwise calls fn with the wrapped
        value and returns the result.

        Some languages call this operation flatmap.
        """
        ...

    def or_else[**P](
        self,
        fn: Callable[P, Maybe[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[T]:
        """Returns the Maybe if it contains a value, otherwise calls fn and returns the
        result."""
        ...

    def filter[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[T]:
        """Returns Empty if the Maybe is Empty, otherwise calls predicate with the
        wrapped value and returns:

        - Some if predicate returns True
        - Empty if predicate returns False.
        """
        ...

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        """Maps a Maybe[T] to FutureMaybe[R] by applying an async function to a
        contained value (if Some) or returns Empty (if Empty)."""
        ...

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        """Calls an async function with a reference to the contained value if Some.

        Returns the original Maybe as FutureMaybe.
        """
        ...

    def is_some_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns Future-wrapped true if the Maybe is a Some and the value inside of it
        matches a async predicate."""
        ...

    def is_empty_or_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns Future-wrapped true if the Maybe is a Empty or the value inside of it
        matches a async predicate."""
        ...

    def and_then_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Maybe[R]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        """Returns Empty if the Maybe is Empty, otherwise calls an async fn with the
        wrapped value and returns the result.

        Some languages call this operation flatmap.
        """
        ...

    def or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[Maybe[T]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        """Returns the Maybe as FutureMaybe if it contains a value, otherwise calls an
        async fn and returns the result."""
        ...

    def filter_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        """Returns Empty as FutureMaybe if the Maybe is Empty, otherwise calls an async
        predicate with the wrapped value and returns:

        - Some if predicate returns True
        - Empty if predicate returns False.
        """
        ...


@dataclass(slots=True, frozen=True)
class Some[T](Maybe[T]):
    internal: T

    @staticmethod
    def from_optional[V](value: V | None) -> Maybe[V]:
        """Construct a new Maybe from passed value.

        If value is None, returns Empty, otherwise wraps value into Some.
        """
        return Some(value) if value is not None else Empty()

    @staticmethod
    def from_if[**P, V](
        value: V,
        fn: Callable[Concatenate[V, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[V]:
        """Constructs a new Maybe from passed value, wrapped into Some if predicate is
        True, otherwise returns Empty."""
        if fn(value, *args, **kwargs):
            return Some(value)

        return Empty()

    def as_maybe(self) -> Maybe[T]:
        return self

    def unwrap(self, **_) -> Any:
        return self.internal

    def unwrap_or(self, /, default: T) -> T:
        return self.internal

    def unwrap_or_none(self) -> T | None:
        return self.internal

    def unwrap_or_else[**P](
        self,
        fn: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        return self.internal

    def unwrap_or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[T]:
        return f.Future.from_(self.internal)

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[R]:
        return Some(fn(self.internal, *args, **kwargs))

    def inspect[**P](
        self,
        fn: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[T]:
        fn(self.internal, *args, **kwargs)
        return self

    def is_some(self) -> bool:
        return True

    def is_empty(self) -> bool:
        return False

    def is_some_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return fn(self.internal, *args, **kwargs)

    def is_empty_or[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return fn(self.internal, *args, **kwargs)

    def and_[R](self, other: Maybe[R]) -> Maybe[R]:
        return other

    def or_(self, other: Maybe[T]) -> Maybe[T]:
        return self

    def and_then[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Maybe[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[R]:
        return fn(self.internal, *args, **kwargs)

    def or_else[**P](
        self,
        fn: Callable[P, Maybe[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[T]:
        return self

    def filter[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[T]:
        return self if fn(self.internal, *args, **kwargs) else Empty()

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        return FutureMaybe(_some_map_async(self.internal, fn, *args, **kwargs))

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        return FutureMaybe(_some_inspect_async(self.internal, fn, *args, **kwargs))

    def is_some_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future(fn(self.internal, *args, **kwargs))

    def is_empty_or_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future(fn(self.internal, *args, **kwargs))

    def and_then_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Maybe[R]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        return FutureMaybe(fn(self.internal, *args, **kwargs))

    def or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[Maybe[T]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        return FutureMaybe.from_(self)

    def filter_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        return FutureMaybe(_some_filter_async(self.internal, fn, *args, **kwargs))


async def _some_map_async[T, **P, R](
    value: T,
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Maybe[R]:
    return Some(await fn(value, *args, **kwargs))


async def _some_inspect_async[T, **P](
    value: T,
    fn: Callable[Concatenate[T, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Maybe[T]:
    await fn(value, *args, **kwargs)
    return Some(value)


async def _some_filter_async[T, **P](
    value: T,
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Maybe[T]:
    if await fn(value, *args, **kwargs):
        return Some(value)

    return Empty()


@dataclass(slots=True, frozen=True)
class Empty(Maybe[Any]):
    def as_maybe[T](self, /, _: Type[T]) -> Maybe[T]:
        return self

    def unwrap(self, *args, **kwargs) -> NoReturn:
        raise EmptyUnwrapError(kwargs.get("on_empty", "expected Some, got Empty"))

    def unwrap_or(self, /, default: Any) -> Any:
        return default

    def unwrap_or_none(self) -> Any | None:
        return None

    def unwrap_or_else[**P, T](
        self, fn: Callable[P, T], *args: P.args, **kwargs: P.kwargs
    ) -> T:
        return fn(*args, **kwargs)

    def unwrap_or_else_async[**P, T](
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[T]:
        return f.Future(fn(*args, **kwargs))

    def map[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[R]:
        return self

    def inspect[**P](
        self,
        fn: Callable[Concatenate[Any, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[Any]:
        return self

    def is_some(self) -> bool:
        return False

    def is_empty(self) -> bool:
        return True

    def is_some_and[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return False

    def is_empty_or[**P](
        self,
        fn: Callable[Concatenate[Any, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return True

    def and_[R](self, other: Maybe[R]) -> Maybe[R]:
        return self

    def or_[T](self, other: Maybe[T]) -> Maybe[T]:
        return other

    def and_then[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], Maybe[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[R]:
        return self

    def or_else[**P, T](
        self,
        fn: Callable[P, Maybe[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[T]:
        return fn(*args, **kwargs)

    def filter[**P](
        self,
        fn: Callable[Concatenate[Any, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[Any]:
        return self

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        return FutureMaybe.from_(self)

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[Any]:
        return FutureMaybe.from_(self)

    def is_some_and_async[**P](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future.from_(False)

    def is_empty_or_async[**P](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future.from_(True)

    def and_then_async[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[Maybe[R]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        return FutureMaybe.from_(self)

    def or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[Maybe[Any]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[Any]:
        return FutureMaybe(fn(*args, **kwargs))

    def filter_async[**P](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[Any]:
        return FutureMaybe.from_(self)


@dataclass(slots=True, frozen=True)
class FutureMaybe[T]:
    internal: f.Future[Maybe[T]]

    def __init__(self, internal: Awaitable[Maybe[T]]) -> None:
        object.__setattr__(
            self,
            "internal",
            f.Future(internal) if not isinstance(internal, f.Future) else internal,
        )

    @staticmethod
    def from_[V](value: Maybe[V]) -> FutureMaybe[V]:
        return FutureMaybe(f.Future.from_(value))

    def __await__(self) -> f.Generator[Any, Any, Maybe[T]]:
        return self.internal.__await__()

    @overload
    def unwrap(self, *, on_empty: str = "expected Some, got Empty") -> f.Future[T]:
        """Returns the contained Some value.

        Because this function may raise EmptyUnwrapError, its use is generally
        discouraged.

        Instead, prefer to use pattern matching and handle the Empty case explicitly, or
        call unwrap_or, unwrap_or_else.
        """
        ...

    @overload
    def unwrap[R](
        self,
        *,
        as_type: Type[R],
        on_empty: str = "expected Some, got Empty",
    ) -> f.Future[R]:
        """Returns the contained Some value casted to passed type.

        Because this function may raise EmptyUnwrapError, its use is generally
        discouraged.

        Instead, prefer to use pattern matching and handle the Empty case explicitly, or
        call unwrap_or, unwrap_or_else.

        No actual casting is performed, type change affects only type checkers.
        """
        ...

    def unwrap(self, **kwargs) -> Any:
        return self.internal.map(maybe.unwrap, **kwargs)  # type: ignore

    def unwrap_or(self, /, other: T) -> f.Future[T]:
        """Returns the contained Some value or a provided default.

        Arguments passed to unwrap_or are eagerly evaluated; if you are passing the
        result of a function call, it is recommended to use unwrap_or_else, which is
        lazily evaluated.
        """
        return self.internal.map(maybe.unwrap_or, other)

    def unwrap_or_none(self) -> f.Future[T | None]:
        """Returns the contained Some value or None."""
        return self.internal.map(maybe.unwrap_or_none)

    def unwrap_or_else[**P](
        self,
        fn: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[T]:
        """Returns the contained Some value or computes it from a sync closure."""
        return self.internal.map(maybe.unwrap_or_else, fn, *args, **kwargs)

    def unwrap_or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[T]:
        """Returns the contained Some value or computes it from a async closure."""
        return self.internal.map_async(maybe.unwrap_or_else_async, fn, *args, **kwargs)

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        """Maps a Maybe[T] to Maybe[R] by applying a function to a contained value (if
        Some) or returns Empty (if Empty)."""
        return FutureMaybe(self.internal.map(maybe.map, fn, *args, **kwargs))

    def inspect[**P](
        self,
        fn: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        """Calls a function with a reference to the contained value if Some.

        Returns the original Maybe.
        """
        return FutureMaybe(self.internal.map(maybe.inspect, fn, *args, **kwargs))

    def is_some(self) -> f.Future[bool]:
        """Returns true if the Maybe is a Some value."""
        return self.internal.map(maybe.is_some)

    def is_empty(self) -> f.Future[bool]:
        """Returns true if the Maybe is a Empty value."""
        return self.internal.map(maybe.is_empty)

    def is_some_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns true if the Maybe is a Some and the value inside of it matches a
        predicate."""
        return self.internal.map(maybe.is_some_and, fn, *args, **kwargs)

    def is_empty_or[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns true if the Maybe is a Empty or the value inside of it matches a
        predicate."""
        return self.internal.map(maybe.is_empty_or, fn, *args, **kwargs)

    def and_[R](self, other: Maybe[R]) -> FutureMaybe[R]:
        """Returns Empty if the Maybe is Empty, otherwise returns other.

        Arguments passed to and_ are eagerly evaluated; if you are passing the result of
        a function call, it is recommended to use and_then, which is lazily evaluated.
        """
        return FutureMaybe(self.internal.map(maybe.and_, other))

    def or_(self, other: Maybe[T]) -> FutureMaybe[T]:
        """Returns the Maybe if it contains a value, otherwise returns other.

        Arguments passed to or_ are eagerly evaluated; if you are passing the result of
        a function call, it is recommended to use or_else, which is lazily evaluated.
        """
        return FutureMaybe(self.internal.map(maybe.or_, other))

    def and_then[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Maybe[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        """Returns Empty if the Maybe is Empty, otherwise calls fn with the wrapped
        value and returns the result.

        Some languages call this operation flatmap.
        """
        return FutureMaybe(self.internal.map(maybe.and_then, fn, *args, **kwargs))

    def or_else[**P](
        self,
        fn: Callable[P, Maybe[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        """Returns the Maybe if it contains a value, otherwise calls fn and returns the
        result."""
        return FutureMaybe(self.internal.map(maybe.or_else, fn, *args, **kwargs))

    def filter[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        """Returns Empty if the Maybe is Empty, otherwise calls predicate with the
        wrapped value and returns:

        - Some if predicate returns True
        - Empty if predicate returns False.
        """
        return FutureMaybe(self.internal.map(maybe.filter, fn, *args, **kwargs))

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        """Maps a Maybe[T] to FutureMaybe[R] by applying an async function to a
        contained value (if Some) or returns Empty (if Empty)."""
        return FutureMaybe(
            self.internal.map_async(maybe.map_async, fn, *args, **kwargs)
        )

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        """Calls an async function with a reference to the contained value if Some.

        Returns the original Maybe as FutureMaybe.
        """
        return FutureMaybe(
            self.internal.map_async(maybe.inspect_async, fn, *args, **kwargs)
        )

    def is_some_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns Future-wrapped true if the Maybe is a Some and the value inside of it
        matches a async predicate."""
        return self.internal.map_async(maybe.is_some_and_async, fn, *args, **kwargs)

    def is_empty_or_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns Future-wrapped true if the Maybe is a Empty or the value inside of it
        matches a async predicate."""
        return self.internal.map_async(maybe.is_empty_or_async, fn, *args, **kwargs)

    def and_then_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Maybe[R]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        """Returns Empty if the Maybe is Empty, otherwise calls an async fn with the
        wrapped value and returns the result.

        Some languages call this operation flatmap.
        """
        return FutureMaybe(
            self.internal.map_async(maybe.and_then_async, fn, *args, **kwargs)
        )

    def or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[Maybe[T]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        """Returns the Maybe as FutureMaybe if it contains a value, otherwise calls an
        async fn and returns the result."""
        return FutureMaybe(
            self.internal.map_async(maybe.or_else_async, fn, *args, **kwargs)
        )

    def filter_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        """Returns Empty as FutureMaybe if the Maybe is Empty, otherwise calls an async
        predicate with the wrapped value and returns:

        - Some if predicate returns True
        - Empty if predicate returns False.
        """
        return FutureMaybe(
            self.internal.map_async(maybe.filter_async, fn, *args, **kwargs)
        )
