from typing import Any, Awaitable, Callable, Concatenate, Type, overload

from . import _future as f, _result as r

__all__ = (
    "and_",
    "and_then",
    "and_then_async",
    "inspect",
    "inspect_async",
    "inspect_err",
    "inspect_err_async",
    "is_err",
    "is_err_and",
    "is_err_and_async",
    "is_err_or",
    "is_err_or_async",
    "is_ok",
    "is_ok_and",
    "is_ok_and_async",
    "is_ok_or",
    "is_ok_or_async",
    "map",
    "map_async",
    "map_err",
    "map_err_async",
    "or_",
    "or_else",
    "or_else_async",
    "unwrap",
    "unwrap_err",
    "unwrap_err_or",
    "unwrap_err_or_else",
    "unwrap_err_or_else_async",
    "unwrap_or",
    "unwrap_or_else",
    "unwrap_or_else_async",
)


@overload
def unwrap[T, E, R](
    res: r.Result[T, E],
    *,
    as_type: Type[R],
    on_err: str = "expected Ok, got Err",
) -> R:
    """Returns the contained Ok value casted to passed type.

    Because this function may raise ErrUnwrapError, its use is generally
    discouraged.

    Instead, prefer to use pattern matching and handle the Err case explicitly, or
    call unwrap_or, unwrap_or_else.

    No actual casting is performed, type change affects only type checkers.
    """
    ...


@overload
def unwrap[T, E](res: r.Result[T, E], *, on_err: str = "expected Ok, got Err") -> T:
    """Returns the contained Ok value.

    Because this function may raise ErrUnwrapError, its use is generally
    discouraged.

    Instead, prefer to use pattern matching and handle the Err case explicitly, or
    call unwrap_or, unwrap_or_else.
    """
    ...


def unwrap[T, E](res: r.Result[T, E], **kwargs) -> Any:
    return res.unwrap(**kwargs)


def unwrap_or[T, E](res: r.Result[T, E], /, other: T) -> T:
    """Returns the contained Ok value or a provided other.

    Arguments passed to unwrap_or are eagerly evaluated; if you are passing the
    result of a function call, it is recommended to use unwrap_or_else, which is
    lazily evaluated.
    """
    return res.unwrap_or(other)


def unwrap_or_else[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[P, T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    """Returns the contained Ok value or computes it from a closure."""
    return res.unwrap_or_else(fn, *args, **kwargs)


def unwrap_or_else_async[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[P, Awaitable[T]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[T]:
    """Returns the contained Ok value or computes it from an async closure."""
    return res.unwrap_or_else_async(fn, *args, **kwargs)


@overload
def unwrap_err[T, E, R](
    res: r.Result[T, E],
    *,
    as_type: Type[R],
    on_err: str = "expected Err, got Ok",
) -> R:
    """Returns the contained Err value casted to passed type.

    Because this function may raise OkUnwrapError, its use is generally discouraged.

    Instead, prefer to use pattern matching and handle the Err case explicitly, or
    call unwrap_err_or, unwrap_err_or_else.

    No actual casting is performed, type change affects only type checkers.
    """
    ...


@overload
def unwrap_err[T, E](res: r.Result[T, E], *, on_err: str = "expected Err, got Ok") -> E:
    """Returns the contained Ok value.

    Because this function may raise OkUnwrapError, its use is generally discouraged.

    Instead, prefer to use pattern matching and handle the Err case explicitly, or
    call unwrap_err_or, unwrap_err_or_else.
    """
    ...


def unwrap_err[T, E](res: r.Result[T, E], **kwargs) -> Any:
    return res.unwrap(**kwargs)


def unwrap_err_or[T, E](res: r.Result[T, E], /, other: E) -> E:
    """Returns the contained Err value or a provided other.

    Arguments passed to unwrap_or are eagerly evaluated; if you are passing the
    result of a function call, it is recommended to use unwrap_err_or_else, which is
    lazily evaluated.
    """
    return res.unwrap_err_or(other)


def unwrap_err_or_else[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[P, E],
    *args: P.args,
    **kwargs: P.kwargs,
) -> E:
    """Returns the contained Err value or computes it from a closure."""
    return res.unwrap_err_or_else(fn, *args, **kwargs)


def unwrap_err_or_else_async[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[P, Awaitable[E]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[E]:
    """Returns the contained Err value or computes it from an async closure."""
    return res.unwrap_err_or_else_async(fn, *args, **kwargs)


def map[T, E, **P, R](
    res: r.Result[T, E],
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[R, E]:
    """Maps a Result[T, E] to Result[R, E] by applying a function to a contained Ok
    value, leaving an Err value untouched.

    This function can be used to compose the results of two functions.
    """
    return res.map(fn, *args, **kwargs)


def map_async[T, E, **P, R](
    res: r.Result[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.FutureResult[R, E]:
    """Maps a Result[T, E] to FutureResult[R, E] by applying an async function to a
    contained Ok value, leaving an Err value untouched.

    This function can be used to compose the results of two functions.
    """
    return res.map_async(fn, *args, **kwargs)


def inspect[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[T, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[T, E]:
    """Calls a function with a reference to the contained value if Ok.

    Returns the original res.
    """
    return res.inspect(fn, *args, **kwargs)


def inspect_async[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.FutureResult[T, E]:
    """Calls an async function with a reference to the contained value if Ok.

    Returns the original result as Futureres.
    """
    return res.inspect_async(fn, *args, **kwargs)


def map_err[T, E, **P, R](
    res: r.Result[T, E],
    fn: Callable[Concatenate[E, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[T, R]:
    """Maps a Result[T, E] to Result[T, R] by applying a function to a contained Err
    value, leaving an Ok value untouched.

    This function can be used to pass through a successful result while handling an
    error.
    """
    return res.map_err(fn, *args, **kwargs)


def map_err_async[T, E, **P, R](
    res: r.Result[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.FutureResult[T, R]:
    """Maps a Result[T, E] to FutureResult[T, R] by applying am async function to a
    contained Err value, leaving an Ok value untouched.

    This function can be used to pass through a successful result while handling an
    error.
    """
    return res.map_err_async(fn, *args, **kwargs)


def inspect_err[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[E, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[T, E]:
    """Calls a function with a reference to the contained value if Err.

    Returns the original res.
    """
    return res.inspect_err(fn, *args, **kwargs)


def inspect_err_async[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.FutureResult[T, E]:
    """Calls an async function with a reference to the contained value if Ok.

    Returns the original result as Futureres.
    """
    return res.inspect_err_async(fn, *args, **kwargs)


def and_[T, E, R](res: r.Result[T, E], other: r.Result[R, E]) -> r.Result[R, E]:
    """Returns other if the result is Ok, otherwise returns the Err value of res: r.Result[T, E].

    Arguments passed to and are eagerly evaluated; if you are passing the result of
    a function call, it is recommended to use and_then, which is lazily evaluated.
    """
    return res.and_(other)


def and_then[T, E, **P, R](
    res: r.Result[T, E],
    fn: Callable[Concatenate[T, P], r.Result[R, E]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[R, E]:
    """Calls a function if the result is Ok, otherwise returns the Err value of
    res: r.Result[T, E].

    This function can be used for control flow based on Result values.
    """
    return res.and_then(fn, *args, **kwargs)


def and_then_async[T, E, **P, R](
    res: r.Result[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[r.Result[R, E]]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.FutureResult[R, E]:
    """Calls an async function if the result is Ok, otherwise returns the Err value
    of res: r.Result[T, E].

    This function can be used for control flow based on Result values.
    """
    return res.and_then_async(fn, *args, **kwargs)


def or_[T, E, R](res: r.Result[T, E], other: r.Result[T, R]) -> r.Result[T, R]:
    """Returns other if the result is Err, otherwise returns the Ok value of res: r.Result[T, E].

    Arguments passed to or are eagerly evaluated; if you are passing the result of a
    function call, it is recommended to use or_else, which is lazily evaluated.
    """
    return res.or_(other)


def or_else[T, E, **P, R](
    res: r.Result[T, E],
    fn: Callable[Concatenate[E, P], r.Result[T, R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[T, R]:
    """Calls a function if the result is Err, otherwise returns the Ok value of
    res: r.Result[T, E].

    This function can be used for control flow based on result values.
    """
    return res.or_else(fn, *args, **kwargs)


def or_else_async[T, E, **P, R](
    res: r.Result[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[r.Result[T, R]]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.FutureResult[T, R]:
    """Calls an async function if the result is Err, otherwise returns the Ok value
    of res: r.Result[T, E].

    This function can be used for control flow based on result values.
    """
    return res.or_else_async(fn, *args, **kwargs)


def is_ok[T, E](res: r.Result[T, E]) -> bool:
    """Returns True if the result is Ok."""
    return res.is_ok()


def is_ok_and[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    """Returns True if the result is Ok and the value inside of it matches a
    predicate."""
    return res.is_ok_and(fn, *args, **kwargs)


def is_ok_and_async[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[bool]:
    """Returns True if the result is Ok and the value inside of it matches an async
    predicate."""
    return res.is_ok_and_async(fn, *args, **kwargs)


def is_ok_or[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[E, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    """Returns True if the result is Ok or the value inside of Err matches a
    predicate."""
    return res.is_ok_or(fn, *args, **kwargs)


def is_ok_or_async[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[bool]:
    """Returns True if the result is Ok or the value inside of Err matches an async
    predicate."""
    return res.is_ok_or_async(fn, *args, **kwargs)


def is_err[T, E](res: r.Result[T, E]) -> bool:
    """Returns True if the result is Err."""
    return res.is_err()


def is_err_and[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[E, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    """Returns True if the result is Err and the value inside of it matches a
    predicate."""
    return res.is_err_and(fn, *args, **kwargs)


def is_err_and_async[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[bool]:
    """Returns True if the result is Err and the value inside of it matches an async
    predicate."""
    return res.is_err_and_async(fn, *args, **kwargs)


def is_err_or[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    """Returns True if the result is Err or the value inside of Ok matches a
    predicate."""
    return res.is_err_or(fn, *args, **kwargs)


def is_err_or_async[T, E, **P](
    res: r.Result[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> f.Future[bool]:
    """Returns True if the result is Err or the value inside of Ok matches an async
    predicate."""
    return res.is_err_or_async(fn, *args, **kwargs)
