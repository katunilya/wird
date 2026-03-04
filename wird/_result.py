from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    Concatenate,
    Generator,
    Protocol,
    Type,
    overload,
)

from . import _future as f, result

__all__ = (
    "Err",
    "ErrUnwrapError",
    "FutureResult",
    "Ok",
    "OkUnwrapError",
    "Result",
)


class ErrUnwrapError(ValueError): ...


class OkUnwrapError(ValueError): ...


class Result[T, E](Protocol):
    @overload
    def unwrap[R](
        self,
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
    def unwrap(self, *, on_err: str = "expected Ok, got Err") -> T:
        """Returns the contained Ok value.

        Because this function may raise ErrUnwrapError, its use is generally
        discouraged.

        Instead, prefer to use pattern matching and handle the Err case explicitly, or
        call unwrap_or, unwrap_or_else.
        """
        ...

    def unwrap_or(self, /, other: T) -> T:
        """Returns the contained Ok value or a provided other.

        Arguments passed to unwrap_or are eagerly evaluated; if you are passing the
        result of a function call, it is recommended to use unwrap_or_else, which is
        lazily evaluated.
        """
        ...

    def unwrap_or_else[**P](
        self,
        fn: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        """Returns the contained Ok value or computes it from a closure."""
        ...

    def unwrap_or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[T]:
        """Returns the contained Ok value or computes it from an async closure."""
        ...

    @overload
    def unwrap_err[R](
        self,
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
    def unwrap_err(self, *, on_err: str = "expected Err, got Ok") -> E:
        """Returns the contained Ok value.

        Because this function may raise OkUnwrapError, its use is generally discouraged.

        Instead, prefer to use pattern matching and handle the Err case explicitly, or
        call unwrap_err_or, unwrap_err_or_else.
        """
        ...

    def unwrap_err_or(self, /, other: E) -> E:
        """Returns the contained Err value or a provided other.

        Arguments passed to unwrap_or are eagerly evaluated; if you are passing the
        result of a function call, it is recommended to use unwrap_err_or_else, which is
        lazily evaluated.
        """
        ...

    def unwrap_err_or_else[**P](
        self,
        fn: Callable[P, E],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> E:
        """Returns the contained Err value or computes it from a closure."""
        ...

    def unwrap_err_or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[E]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[E]:
        """Returns the contained Err value or computes it from an async closure."""
        ...

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[R, E]:
        """Maps a Result[T, E] to Result[R, E] by applying a function to a contained Ok
        value, leaving an Err value untouched.

        This function can be used to compose the results of two functions.
        """
        ...

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, E]:
        """Maps a Result[T, E] to FutureResult[R, E] by applying an async function to a
        contained Ok value, leaving an Err value untouched.

        This function can be used to compose the results of two functions.
        """
        ...

    def inspect[**P](
        self,
        fn: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, E]:
        """Calls a function with a reference to the contained value if Ok.

        Returns the original result.
        """
        ...

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        """Calls an async function with a reference to the contained value if Ok.

        Returns the original result as FutureResult.
        """
        ...

    def map_err[**P, R](
        self,
        fn: Callable[Concatenate[E, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, R]:
        """Maps a Result[T, E] to Result[T, R] by applying a function to a contained Err
        value, leaving an Ok value untouched.

        This function can be used to pass through a successful result while handling an
        error.
        """
        ...

    def map_err_async[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, R]:
        """Maps a Result[T, E] to FutureResult[T, R] by applying am async function to a
        contained Err value, leaving an Ok value untouched.

        This function can be used to pass through a successful result while handling an
        error.
        """
        ...

    def inspect_err[**P](
        self,
        fn: Callable[Concatenate[E, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, E]:
        """Calls a function with a reference to the contained value if Err.

        Returns the original result.
        """
        ...

    def inspect_err_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        """Calls an async function with a reference to the contained value if Ok.

        Returns the original result as FutureResult.
        """
        ...

    def and_[R](self, other: Result[R, E]) -> Result[R, E]:
        """Returns other if the result is Ok, otherwise returns the Err value of self.

        Arguments passed to and are eagerly evaluated; if you are passing the result of
        a function call, it is recommended to use and_then, which is lazily evaluated.
        """
        ...

    def and_then[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Result[R, E]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[R, E]:
        """Calls a function if the result is Ok, otherwise returns the Err value of
        self.

        This function can be used for control flow based on Result values.
        """
        ...

    def and_then_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Result[R, E]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, E]:
        """Calls an async function if the result is Ok, otherwise returns the Err value
        of self.

        This function can be used for control flow based on Result values.
        """
        ...

    def or_[R](self, other: Result[T, R]) -> Result[T, R]:
        """Returns other if the result is Err, otherwise returns the Ok value of self.

        Arguments passed to or are eagerly evaluated; if you are passing the result of a
        function call, it is recommended to use or_else, which is lazily evaluated.
        """
        ...

    def or_else[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Result[T, R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, R]:
        """Calls a function if the result is Err, otherwise returns the Ok value of
        self.

        This function can be used for control flow based on result values.
        """
        ...

    def or_else_async[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[Result[T, R]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, R]:
        """Calls an async function if the result is Err, otherwise returns the Ok value
        of self.

        This function can be used for control flow based on result values.
        """
        ...

    def is_ok(self) -> bool:
        """Returns True if the result is Ok."""
        ...

    def is_ok_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        """Returns True if the result is Ok and the value inside of it matches a
        predicate."""
        ...

    def is_ok_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Ok and the value inside of it matches an async
        predicate."""
        ...

    def is_ok_or[**P](
        self,
        fn: Callable[Concatenate[E, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        """Returns True if the result is Ok or the value inside of Err matches a
        predicate."""
        ...

    def is_ok_or_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Ok or the value inside of Err matches an async
        predicate."""
        ...

    def is_err(self) -> bool:
        """Returns True if the result is Err."""
        ...

    def is_err_and[**P](
        self,
        fn: Callable[Concatenate[E, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        """Returns True if the result is Err and the value inside of it matches a
        predicate."""
        ...

    def is_err_and_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Err and the value inside of it matches an async
        predicate."""
        ...

    def is_err_or[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        """Returns True if the result is Err or the value inside of Ok matches a
        predicate."""
        ...

    def is_err_or_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Err or the value inside of Ok matches an async
        predicate."""
        ...


@dataclass(slots=True, frozen=True)
class Ok[T](Result[T, Any]):
    internal: T

    def as_result[E](self, _: Type[E]) -> Result[T, E]:
        return self

    @overload
    def unwrap[R](
        self,
        *,
        as_type: Type[R],
        on_err: str = "expected Ok, got Err",
    ) -> R: ...

    @overload
    def unwrap(self, *, on_err: str = "expected Ok, got Err") -> T: ...

    def unwrap(self, **kwargs) -> Any:
        return self.internal

    def unwrap_or(self, /, other: T) -> T:
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

    @overload
    def unwrap_err[R](
        self,
        *,
        as_type: Type[R],
        on_err: str = "expected Err, got Ok",
    ) -> R: ...

    @overload
    def unwrap_err(self, *, on_err: str = "expected Err, got Ok") -> T: ...

    def unwrap_err(self, **kwargs) -> Any:
        raise OkUnwrapError(kwargs.get("on_ok", "expected Ok, got Err"))

    def unwrap_err_or[E](self, /, other: E) -> E:
        return other

    def unwrap_err_or_else[E, **P](
        self,
        fn: Callable[P, E],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> E:
        return fn(*args, **kwargs)

    def unwrap_err_or_else_async[E, **P](
        self,
        fn: Callable[P, Awaitable[E]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[E]:
        return f.Future(fn(*args, **kwargs))

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[R, Any]:
        return Ok(fn(self.internal, *args, **kwargs))

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, Any]:
        return FutureResult(_ok_map_async(self.internal, fn, *args, **kwargs))

    def inspect[**P](
        self,
        fn: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, Any]:
        fn(self.internal, *args, **kwargs)
        return self

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, Any]:
        return FutureResult(_ok_inspect_async(self.internal, fn, *args, **kwargs))

    def map_err[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, R]:
        return self

    def map_err_async[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, R]:
        return FutureResult.from_(self)

    def inspect_err[**P](
        self,
        fn: Callable[Concatenate[Any, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, Any]:
        return self

    def inspect_err_async[**P](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, Any]:
        return FutureResult.from_(self)

    def and_[R](self, other: Result[R, Any]) -> Result[R, Any]:
        return other

    def and_then[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Result[R, Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[R, Any]:
        return fn(self.internal, *args, **kwargs)

    def and_then_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Result[R, Any]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, Any]:
        return FutureResult(fn(self.internal, *args, **kwargs))

    def or_[R](self, other: Result[T, R]) -> Result[T, R]:
        return self

    def or_else[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], Result[T, R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, R]:
        return self

    def or_else_async[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[Result[T, R]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, R]:
        return FutureResult.from_(self)

    def is_ok(self) -> bool:
        return True

    def is_ok_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return fn(self.internal, *args, **kwargs)

    def is_ok_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future(fn(self.internal, *args, **kwargs))

    def is_ok_or[**P](
        self,
        fn: Callable[Concatenate[Any, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return True

    def is_ok_or_async[**P](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future.from_(True)

    def is_err(self) -> bool:
        return False

    def is_err_and[**P](
        self,
        fn: Callable[Concatenate[Any, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return False

    def is_err_and_async[**P](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future.from_(False)

    def is_err_or[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return fn(self.internal, *args, **kwargs)

    def is_err_or_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future(fn(self.internal, *args, **kwargs))


async def _ok_map_async[T, **P, R](
    value: T,
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[R, Any]:
    return Ok(await fn(value, *args, **kwargs))


async def _ok_inspect_async[T, **P](
    value: T,
    fn: Callable[Concatenate[T, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, Any]:
    await fn(value, *args, **kwargs)
    return Ok(value)


@dataclass(slots=True, frozen=True)
class Err[E](Result[Any, E]):
    internal: E

    def as_result[T](self, _: Type[T]) -> Result[T, E]:
        return self

    @overload
    def unwrap[R](
        self,
        *,
        as_type: Type[R],
        on_err: str = "expected Ok, got Err",
    ) -> R: ...

    @overload
    def unwrap(self, *, on_err: str = "expected Ok, got Err") -> Any: ...

    def unwrap(self, **kwargs) -> Any:
        raise ErrUnwrapError(kwargs.get("on_err", "expected Ok, got Err"))

    def unwrap_or[T](self, /, other: T) -> T:
        return other

    def unwrap_or_else[T, **P](
        self,
        fn: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        return fn(*args, **kwargs)

    def unwrap_or_else_async[T, **P](
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[T]:
        return f.Future(fn(*args, **kwargs))

    @overload
    def unwrap_err[R](
        self,
        *,
        as_type: Type[R],
        on_err: str = "expected Err, got Ok",
    ) -> R: ...

    @overload
    def unwrap_err(self, *, on_err: str = "expected Err, got Ok") -> E: ...

    def unwrap_err(self, **kwargs) -> Any:
        return self.internal

    def unwrap_err_or(self, /, other: E) -> E:
        return self.internal

    def unwrap_err_or_else[**P](
        self,
        fn: Callable[P, E],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> E:
        return self.internal

    def unwrap_err_or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[E]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[E]:
        return f.Future.from_(self.internal)

    def map[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[R, E]:
        return self

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, E]:
        return FutureResult.from_(self)

    def inspect[**P](
        self,
        fn: Callable[Concatenate[Any, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[Any, E]:
        return self

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[Any, E]:
        return FutureResult.from_(self)

    def map_err[**P, R](
        self,
        fn: Callable[Concatenate[E, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[Any, R]:
        return Err(fn(self.internal, *args, **kwargs))

    def map_err_async[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[Any, R]:
        return FutureResult(_err_map_err_async(self.internal, fn, *args, **kwargs))

    def inspect_err[**P](
        self,
        fn: Callable[Concatenate[E, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[Any, E]:
        fn(self.internal, *args, **kwargs)
        return self

    def inspect_err_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[Any, E]:
        return FutureResult(_err_inspect_err_async(self.internal, fn, *args, **kwargs))

    def and_[R](self, other: Result[R, E]) -> Result[R, E]:
        return self

    def and_then[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], Result[R, E]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[R, E]:
        return self

    def and_then_async[**P, R](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[Result[R, E]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, E]:
        return FutureResult.from_(self)

    def or_[R](self, other: Result[Any, R]) -> Result[Any, R]:
        return other

    def or_else[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Result[Any, R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[Any, R]:
        return fn(self.internal, *args, **kwargs)

    def or_else_async[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[Result[Any, R]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[Any, R]:
        return FutureResult(fn(self.internal, *args, **kwargs))

    def is_ok(self) -> bool:
        return False

    def is_ok_and[**P](
        self,
        fn: Callable[Concatenate[Any, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return False

    def is_ok_and_async[**P](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future.from_(False)

    def is_ok_or[**P](
        self,
        fn: Callable[Concatenate[E, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return fn(self.internal, *args, **kwargs)

    def is_ok_or_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future(fn(self.internal, *args, **kwargs))

    def is_err(self) -> bool:
        return True

    def is_err_and[**P](
        self,
        fn: Callable[Concatenate[E, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return fn(self.internal, *args, **kwargs)

    def is_err_and_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future(fn(self.internal, *args, **kwargs))

    def is_err_or[**P](
        self,
        fn: Callable[Concatenate[Any, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return True

    def is_err_or_async[**P](
        self,
        fn: Callable[Concatenate[Any, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        return f.Future.from_(True)


async def _err_map_err_async[E, **P, R](
    value: E,
    fn: Callable[Concatenate[E, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Err[R]:
    return Err(await fn(value, *args, **kwargs))


async def _err_inspect_err_async[E, **P](
    value: E,
    fn: Callable[Concatenate[E, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Err[E]:
    await fn(value, *args, **kwargs)
    return Err(value)


@dataclass(slots=True, frozen=True)
class FutureResult[T, E]:
    internal: f.Future[Result[T, E]]

    def __init__(self, internal: Awaitable[Result[T, E]]) -> None:
        object.__setattr__(
            self,
            "internal",
            f.Future(internal) if not isinstance(internal, f.Future) else internal,
        )

    @staticmethod
    def from_(value: Result[T, E]) -> FutureResult[T, E]:
        return FutureResult(f.Future.from_(value))

    def __await__(self) -> Generator[Any, Any, Result[T, E]]:
        return self.internal.__await__()

    @overload
    def unwrap[R](
        self,
        *,
        as_type: Type[R],
        on_err: str = "expected Ok, got Err",
    ) -> f.Future[R]:
        """Returns the contained Ok value casted to passed type.

        Because this function may raise ErrUnwrapError, its use is generally
        discouraged.

        Instead, prefer to use pattern matching and handle the Err case explicitly, or
        call unwrap_or, unwrap_or_else.

        No actual casting is performed, type change affects only type checkers.
        """
        ...

    @overload
    def unwrap(self, *, on_err: str = "expected Ok, got Err") -> f.Future[T]:
        """Returns the contained Ok value.

        Because this function may raise ErrUnwrapError, its use is generally
        discouraged.

        Instead, prefer to use pattern matching and handle the Err case explicitly, or
        call unwrap_or, unwrap_or_else.
        """
        ...

    def unwrap(self, **kwargs) -> f.Future[Any]:
        return self.internal.map(result.unwrap, **kwargs)  # type: ignore[arg-type]

    def unwrap_or(self, /, other: T) -> f.Future[T]:
        """Returns the contained Ok value or a provided other.

        Arguments passed to unwrap_or are eagerly evaluated; if you are passing the
        result of a function call, it is recommended to use unwrap_or_else, which is
        lazily evaluated.
        """
        return self.internal.map(result.unwrap_or, other)

    def unwrap_or_else[**P](
        self,
        fn: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[T]:
        """Returns the contained Ok value or computes it from a closure."""
        return self.internal.map(result.unwrap_or_else, fn, *args, **kwargs)

    def unwrap_or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[T]:
        """Returns the contained Ok value or computes it from an async closure."""
        return self.internal.map_async(result.unwrap_or_else_async, fn, *args, **kwargs)

    @overload
    def unwrap_err[R](
        self,
        *,
        as_type: Type[R],
        on_err: str = "expected Err, got Ok",
    ) -> f.Future[R]:
        """Returns the contained Err value casted to passed type.

        Because this function may raise OkUnwrapError, its use is generally discouraged.

        Instead, prefer to use pattern matching and handle the Err case explicitly, or
        call unwrap_err_or, unwrap_err_or_else.

        No actual casting is performed, type change affects only type checkers.
        """
        ...

    @overload
    def unwrap_err(self, *, on_err: str = "expected Err, got Ok") -> f.Future[E]:
        """Returns the contained Ok value.

        Because this function may raise OkUnwrapError, its use is generally discouraged.

        Instead, prefer to use pattern matching and handle the Err case explicitly, or
        call unwrap_err_or, unwrap_err_or_else.
        """
        ...

    def unwrap_err(self, **kwargs) -> f.Future[Any]:
        return self.internal.map(result.unwrap_err, **kwargs)  # type: ignore[arg-type]

    def unwrap_err_or(self, /, other: E) -> f.Future[E]:
        """Returns the contained Err value or a provided other.

        Arguments passed to unwrap_or are eagerly evaluated; if you are passing the
        result of a function call, it is recommended to use unwrap_err_or_else, which is
        lazily evaluated.
        """
        return self.internal.map(result.unwrap_err_or, other)

    def unwrap_err_or_else[**P](
        self,
        fn: Callable[P, E],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[E]:
        """Returns the contained Err value or computes it from a closure."""
        return self.internal.map(result.unwrap_err_or_else, fn, *args, **kwargs)

    def unwrap_err_or_else_async[**P](
        self,
        fn: Callable[P, Awaitable[E]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[E]:
        """Returns the contained Err value or computes it from an async closure."""
        return self.internal.map_async(
            result.unwrap_err_or_else_async, fn, *args, **kwargs
        )

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, E]:
        """Maps a Result[T, E] to Result[R, E] by applying a function to a contained Ok
        value, leaving an Err value untouched.

        This function can be used to compose the results of two functions.
        """
        return FutureResult(self.internal.map(result.map, fn, *args, **kwargs))

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, E]:
        """Maps a Result[T, E] to FutureResult[R, E] by applying an async function to a
        contained Ok value, leaving an Err value untouched.

        This function can be used to compose the results of two functions.
        """
        return FutureResult(
            self.internal.map_async(result.map_async, fn, *args, **kwargs)
        )

    def inspect[**P](
        self,
        fn: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        """Calls a function with a reference to the contained value if Ok.

        Returns the original result.
        """
        return FutureResult(self.internal.map(result.inspect, fn, *args, **kwargs))

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        """Calls an async function with a reference to the contained value if Ok.

        Returns the original result as FutureResult.
        """
        return FutureResult(
            self.internal.map_async(result.inspect_async, fn, *args, **kwargs)
        )

    def map_err[**P, R](
        self,
        fn: Callable[Concatenate[E, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, R]:
        """Maps a Result[T, E] to Result[T, R] by applying a function to a contained Err
        value, leaving an Ok value untouched.

        This function can be used to pass through a successful result while handling an
        error.
        """
        return FutureResult(self.internal.map(result.map_err, fn, *args, **kwargs))

    def map_err_async[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, R]:
        """Maps a Result[T, E] to FutureResult[T, R] by applying am async function to a
        contained Err value, leaving an Ok value untouched.

        This function can be used to pass through a successful result while handling an
        error.
        """
        return FutureResult(
            self.internal.map_async(result.map_err_async, fn, *args, **kwargs)
        )

    def inspect_err[**P](
        self,
        fn: Callable[Concatenate[E, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        """Calls a function with a reference to the contained value if Err.

        Returns the original result.
        """
        return FutureResult(self.internal.map(result.inspect_err, fn, *args, **kwargs))

    def inspect_err_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        """Calls an async function with a reference to the contained value if Ok.

        Returns the original result as FutureResult.
        """
        return FutureResult(
            self.internal.map_async(result.inspect_err_async, fn, *args, **kwargs)
        )

    def and_[R](self, other: Result[R, E]) -> FutureResult[R, E]:
        """Returns other if the result is Ok, otherwise returns the Err value of self.

        Arguments passed to and are eagerly evaluated; if you are passing the result of
        a function call, it is recommended to use and_then, which is lazily evaluated.
        """
        return FutureResult(self.internal.map(result.and_, other))

    def and_then[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Result[R, E]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, E]:
        """Calls a function if the result is Ok, otherwise returns the Err value of
        self.

        This function can be used for control flow based on Result values.
        """
        return FutureResult(self.internal.map(result.and_then, fn, *args, **kwargs))

    def and_then_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Result[R, E]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, E]:
        """Calls an async function if the result is Ok, otherwise returns the Err value
        of self.

        This function can be used for control flow based on Result values.
        """
        return FutureResult(
            self.internal.map_async(result.and_then_async, fn, *args, **kwargs)
        )

    def or_[R](self, other: Result[T, R]) -> FutureResult[T, R]:
        """Returns other if the result is Err, otherwise returns the Ok value of self.

        Arguments passed to or are eagerly evaluated; if you are passing the result of a
        function call, it is recommended to use or_else, which is lazily evaluated.
        """
        return FutureResult(self.internal.map(result.or_, other))

    def or_else[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Result[T, R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, R]:
        """Calls a function if the result is Err, otherwise returns the Ok value of
        self.

        This function can be used for control flow based on result values.
        """
        return FutureResult(self.internal.map(result.or_else, fn, *args, **kwargs))

    def or_else_async[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[Result[T, R]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, R]:
        """Calls an async function if the result is Err, otherwise returns the Ok value
        of self.

        This function can be used for control flow based on result values.
        """
        return FutureResult(
            self.internal.map_async(result.or_else_async, fn, *args, **kwargs)
        )

    def is_ok(self) -> f.Future[bool]:
        """Returns True if the result is Ok."""
        return self.internal.map(result.is_ok)

    def is_ok_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Ok and the value inside of it matches a
        predicate."""
        return self.internal.map(result.is_ok_and, fn, *args, **kwargs)

    def is_ok_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Ok and the value inside of it matches an async
        predicate."""
        return self.internal.map_async(result.is_ok_and_async, fn, *args, **kwargs)

    def is_ok_or[**P](
        self,
        fn: Callable[Concatenate[E, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Ok or the value inside of Err matches a
        predicate."""
        return self.internal.map(result.is_ok_or, fn, *args, **kwargs)

    def is_ok_or_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Ok or the value inside of Err matches an async
        predicate."""
        return self.internal.map_async(result.is_ok_or_async, fn, *args, **kwargs)

    def is_err(self) -> f.Future[bool]:
        """Returns True if the result is Err."""
        return self.internal.map(result.is_err)

    def is_err_and[**P](
        self,
        fn: Callable[Concatenate[E, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Err and the value inside of it matches a
        predicate."""
        return self.internal.map(result.is_err_and, fn, *args, **kwargs)

    def is_err_and_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Err and the value inside of it matches an async
        predicate."""
        return self.internal.map_async(result.is_err_and_async, fn, *args, **kwargs)

    def is_err_or[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Err or the value inside of Ok matches a
        predicate."""
        return self.internal.map(result.is_err_or, fn, *args, **kwargs)

    def is_err_or_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> f.Future[bool]:
        """Returns True if the result is Err or the value inside of Ok matches an async
        predicate."""
        return self.internal.map_async(result.is_err_or_async, fn, *args, **kwargs)
