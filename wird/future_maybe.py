from typing import Any, Awaitable, Callable, Concatenate, Type, overload

from . import _future as f, _maybe as m

__all__ = (
    "and_",
    "and_then",
    "and_then_async",
    "filter",
    "filter_async",
    "inspect",
    "inspect_async",
    "is_empty",
    "is_empty_or",
    "is_empty_or_async",
    "is_some",
    "is_some_and",
    "is_some_and_async",
    "map",
    "map_async",
    "or_",
    "or_else",
    "or_else_async",
    "unwrap",
    "unwrap_or",
    "unwrap_or_else",
    "unwrap_or_else_async",
    "unwrap_or_none",
)


@overload
def unwrap[T](
    future_maybe: m.FutureMaybe[T], *, on_empty: str = "expected Some, got Empty"
) -> f.Future[T]:
    """Returns the contained Some value.

    Because this function may raise EmptyUnwrapError, its use is generally
    discouraged.

    Instead, prefer to use pattern matching and handle the Empty case explicitly, or
    call unwrap_or, unwrap_or_else.
    """
    ...


@overload
def unwrap[T, R](
    future_maybe: m.FutureMaybe[T],
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


def unwrap[T](future_maybe: m.FutureMaybe[T], **kwargs) -> Any:
    return future_maybe.unwrap(**kwargs)


def unwrap_or[T](future_maybe: m.FutureMaybe[T], /, other: T) -> f.Future[T]:
    """Returns the contained Some value or a provided default.

    Arguments passed to unwrap_or are eagerly evaluated; if you are passing the
    result of a function call, it is recommended to use unwrap_or_else, which is
    lazily evaluated.
    """
    return future_maybe.unwrap_or(other)


def unwrap_or_none[T](future_maybe: m.FutureMaybe[T]) -> f.Future[T | None]:
    """Returns the contained Some value or None."""
    return future_maybe.unwrap_or_none()


def unwrap_or_else[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[P, T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[T]:
    """Returns the contained Some value or computes it from a sync closure."""
    return future_maybe.unwrap_or_else(fn, *args, **kwargs)


def unwrap_or_else_async[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[P, Awaitable[T]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[T]:
    """Returns the contained Some value or computes it from a async closure."""
    return future_maybe.unwrap_or_else_async(fn, *args, **kwargs)


def map[T, **P, R](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.FutureMaybe[R]:
    """Maps a Maybe[T] to Maybe[R] by applying a function to a contained value (if
    Some) or returns Empty (if Empty)."""
    return future_maybe.map(fn, *args, **kwargs)


def inspect[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.FutureMaybe[T]:
    """Calls a function with a reference to the contained value if Some.

    Returns the original Maybe.
    """
    return future_maybe.inspect_async(fn, *args, **kwargs)


def is_some[T](future_maybe: m.FutureMaybe[T]) -> f.Future[bool]:
    """Returns true if the Maybe is a Some value."""
    return future_maybe.is_some()


def is_empty[T](future_maybe: m.FutureMaybe[T]) -> f.Future[bool]:
    """Returns true if the Maybe is a Empty value."""
    return future_maybe.is_empty()


def is_some_and[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[bool]:
    """Returns true if the Maybe is a Some and the value inside of it matches a
    predicate."""
    return future_maybe.is_some_and(fn, *args, **kwargs)


def is_empty_or[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[bool]:
    """Returns true if the Maybe is a Empty or the value inside of it matches a
    predicate."""
    return future_maybe.is_empty_or(fn, *args, **kwargs)


def and_[T, R](future_maybe: m.FutureMaybe[T], other: m.Maybe[R]) -> m.FutureMaybe[R]:
    """Returns Empty if the Maybe is Empty, otherwise returns other.

    Arguments passed to and_ are eagerly evaluated; if you are passing the result of
    a function call, it is recommended to use and_then, which is lazily evaluated.
    """
    return future_maybe.and_(other)


def or_[T](future_maybe: m.FutureMaybe[T], other: m.Maybe[T]) -> m.FutureMaybe[T]:
    """Returns the Maybe if it contains a value, otherwise returns other.

    Arguments passed to or_ are eagerly evaluated; if you are passing the result of
    a function call, it is recommended to use or_else, which is lazily evaluated.
    """
    return future_maybe.or_(other)


def and_then[T, **P, R](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], m.Maybe[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.FutureMaybe[R]:
    """Returns Empty if the Maybe is Empty, otherwise calls fn with the wrapped
    value and returns the result.

    Some languages call this operation flatmap.
    """
    return future_maybe.and_then(fn, *args, **kwargs)


def or_else[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[P, m.Maybe[T]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.FutureMaybe[T]:
    """Returns the Maybe if it contains a value, otherwise calls fn and returns the
    result."""
    return future_maybe.or_else(fn, *args, **kwargs)


def filter[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.FutureMaybe[T]:
    """Returns Empty if the Maybe is Empty, otherwise calls predicate with the
    wrapped value and returns:

    - Some if predicate returns True
    - Empty if predicate returns False.
    """
    return future_maybe.filter(fn, *args, **kwargs)


def map_async[T, **P, R](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.FutureMaybe[R]:
    """Maps a Maybe[T] to m.FutureMaybe[R] by applying an async function to a
    contained value (if Some) or returns Empty (if Empty)."""
    return future_maybe.map_async(fn, *args, **kwargs)


def inspect_async[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.FutureMaybe[T]:
    """Calls an async function with a reference to the contained value if Some.

    Returns the original Maybe as m.FutureMaybe.
    """
    return future_maybe.inspect_async(fn, *args, **kwargs)


def is_some_and_async[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[bool]:
    """Returns Future-wrapped true if the Maybe is a Some and the value inside of it
    matches a async predicate."""
    return future_maybe.is_some_and_async(fn, *args, **kwargs)


def is_empty_or_async[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[bool]:
    """Returns Future-wrapped true if the Maybe is a Empty or the value inside of it
    matches a async predicate."""
    return future_maybe.is_empty_or_async(fn, *args, **kwargs)


def and_then_async[T, **P, R](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[m.Maybe[R]]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.FutureMaybe[R]:
    """Returns Empty if the Maybe is Empty, otherwise calls an async fn with the
    wrapped value and returns the result.

    Some languages call this operation flatmap.
    """
    return future_maybe.and_then_async(fn, *args, **kwargs)


def or_else_async[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[P, Awaitable[m.Maybe[T]]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.FutureMaybe[T]:
    """Returns the Maybe as m.FutureMaybe if it contains a value, otherwise calls an
    async fn and returns the result."""
    return m.FutureMaybe(future_maybe.or_else_async(fn, *args, **kwargs))


def filter_async[T, **P](
    future_maybe: m.FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.FutureMaybe[T]:
    """Returns Empty as m.FutureMaybe if the Maybe is Empty, otherwise calls an async
    predicate with the wrapped value and returns:

    - Some if predicate returns True
    - Empty if predicate returns False.
    """
    return future_maybe.filter_async(fn, *args, **kwargs)
