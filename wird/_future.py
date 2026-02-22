from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    Concatenate,
    Generator,
    Type,
    overload,
)

__all__ = ("Future",)


@dataclass(slots=True, frozen=True)
class Future[T]:
    internal: Awaitable[T]

    @staticmethod
    def from_[V](value: V) -> Future[V]:
        async def _identity() -> V:
            return value

        return Future(_identity())

    @overload
    def unwrap(self) -> Awaitable[T]: ...

    @overload
    def unwrap[R](self, *, as_type: Type[R]) -> Awaitable[R]: ...

    def unwrap(self, **_) -> Awaitable[Any]:
        return self.internal

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:
        return Future(_map(self.internal, fn, *args, **kwargs))

    def inspect[**P](
        self,
        fn: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[T]:
        return Future(_inspect(self.internal, fn, *args, **kwargs))

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:
        return Future(_map_async(self.internal, fn, *args, **kwargs))

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[T]:
        return Future(_inspect_async(self.internal, fn, *args, **kwargs))

    def __await__(self) -> Generator[Any, Any, T]:
        return self.internal.__await__()


async def _map[T, **P, R](
    value: Awaitable[T],
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    return fn(await value, *args, **kwargs)


async def _inspect[T, **P](
    value: Awaitable[T],
    fn: Callable[Concatenate[T, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    _value = await value
    fn(_value, *args, **kwargs)
    return _value


async def _map_async[T, **P, R](
    value: Awaitable[T],
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    return await fn(await value, *args, **kwargs)


async def _inspect_async[T, **P](
    value: Awaitable[T],
    fn: Callable[Concatenate[T, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    _value = await value
    await fn(_value, *args, **kwargs)
    return _value
