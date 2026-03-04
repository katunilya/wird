import operator

import pytest

from wird import Empty, Future, Maybe, Some
from wird._maybe import EmptyUnwrapError, FutureMaybe


async def test_some_unwraps() -> None:
    m = Some(1).as_maybe()

    assert m.unwrap() == 1
    assert m.unwrap_or(2) == 1
    assert m.unwrap_or_none() == 1
    assert m.unwrap_or_else(lambda: 2) == 1
    assert await m.unwrap_or_else_async(lambda: Future.from_(2)) == 1

    assert await FutureMaybe.from_(m).unwrap() == 1
    assert await FutureMaybe.from_(m).unwrap_or(2) == 1
    assert await FutureMaybe.from_(m).unwrap_or_none() == 1
    assert await FutureMaybe.from_(m).unwrap_or_else(lambda: 2) == 1
    assert await FutureMaybe.from_(m).unwrap_or_else_async(lambda: Future.from_(2)) == 1


async def test_empty_unwraps() -> None:
    m = Empty().as_maybe(int)

    with pytest.raises(EmptyUnwrapError, match="expected Some, got Empty"):
        m.unwrap()

    with pytest.raises(EmptyUnwrapError, match="on empty"):
        m.unwrap(on_empty="on empty")

    assert m.unwrap_or(2) == 2
    assert m.unwrap_or_none() is None
    assert m.unwrap_or_else(lambda: 2) == 2
    assert await m.unwrap_or_else_async(lambda: Future.from_(2)) == 2

    with pytest.raises(EmptyUnwrapError, match="expected Some, got Empty"):
        await FutureMaybe.from_(m).unwrap()

    with pytest.raises(EmptyUnwrapError, match="on empty"):
        await FutureMaybe.from_(m).unwrap(on_empty="on empty")

    assert await FutureMaybe.from_(m).unwrap_or(2) == 2
    assert await FutureMaybe.from_(m).unwrap_or_none() is None
    assert await FutureMaybe.from_(m).unwrap_or_else(lambda: 2) == 2
    assert await FutureMaybe.from_(m).unwrap_or_else_async(lambda: Future.from_(2)) == 2


@pytest.mark.parametrize(
    ("maybe", "target"),
    [
        (Some(1), Some(5)),
        (Empty(), Empty()),
    ],
)
async def test_maybe_map(maybe: Maybe[int], target: Maybe[int]) -> None:
    assert (
        await maybe.map(operator.add, 1)
        .map_async(lambda x: Future.from_(x + 1))
        .map(operator.add, 1)
        .map_async(lambda x: Future.from_(x + 1))
        == target
    )


@pytest.mark.parametrize(
    ("maybe", "target"),
    [
        (Some({}), Some({"a": 1, "b": 2, "c": 3, "d": 4})),
        (Empty(), Empty()),
    ],
)
async def test_maybe_inspect(maybe: Maybe[dict], target: Maybe[dict]) -> None:
    async def set_item(data: dict, key: str, value: int) -> None:
        data[key] = value

    assert await (
        maybe.inspect(operator.setitem, "a", 1)
        .inspect_async(set_item, "b", 2)
        .inspect(operator.setitem, "c", 3)
        .inspect_async(set_item, "d", 4)
    )


async def test_some_predicates() -> None:
    m = Some(1).as_maybe()

    assert m.is_some()
    assert not m.is_empty()
    assert m.is_some_and(lambda x: x % 2 == 1)
    assert m.is_empty_or(lambda x: x % 2 == 1)
    assert await m.is_some_and_async(lambda x: Future.from_(x % 2 == 1))
    assert await m.is_empty_or_async(lambda x: Future.from_(x % 2 == 1))

    assert await FutureMaybe.from_(m).is_some()
    assert not await FutureMaybe.from_(m).is_empty()
    assert await FutureMaybe.from_(m).is_some_and(lambda x: x % 2 == 1)
    assert await FutureMaybe.from_(m).is_empty_or(lambda x: x % 2 == 1)
    assert await FutureMaybe.from_(m).is_some_and_async(
        lambda x: Future.from_(x % 2 == 1)
    )
    assert await FutureMaybe.from_(m).is_empty_or_async(
        lambda x: Future.from_(x % 2 == 1)
    )


async def test_empty_predicates() -> None:
    m = Empty().as_maybe(int)

    assert not m.is_some()
    assert m.is_empty()
    assert not m.is_some_and(lambda x: x % 2 == 1)
    assert m.is_empty_or(lambda x: x % 2 == 1)
    assert not await m.is_some_and_async(lambda x: Future.from_(x % 2 == 1))
    assert await m.is_empty_or_async(lambda x: Future.from_(x % 2 == 1))

    assert not await FutureMaybe.from_(m).is_some()
    assert await FutureMaybe.from_(m).is_empty()
    assert not await FutureMaybe.from_(m).is_some_and(lambda x: x % 2 == 1)
    assert await FutureMaybe.from_(m).is_empty_or(lambda x: x % 2 == 1)
    assert not await FutureMaybe.from_(m).is_some_and_async(
        lambda x: Future.from_(x % 2 == 1)
    )
    assert await FutureMaybe.from_(m).is_empty_or_async(
        lambda x: Future.from_(x % 2 == 1)
    )


async def test_some_and() -> None:
    m = Some(1).as_maybe()

    assert m.and_(Some(2)) == Some(2)
    assert m.and_(Empty()) == Empty()
    assert m.and_then(lambda _: Some(2)) == Some(2)
    assert m.and_then(lambda _: Empty()) == Empty()
    assert await m.and_then_async(lambda _: Future.from_(Some(2))) == Some(2)
    assert await m.and_then_async(lambda _: Future.from_(Empty())) == Empty()

    assert await FutureMaybe.from_(m).and_(Some(2)) == Some(2)
    assert await FutureMaybe.from_(m).and_(Empty()) == Empty()
    assert await FutureMaybe.from_(m).and_then(lambda _: Some(2)) == Some(2)
    assert await FutureMaybe.from_(m).and_then(lambda _: Empty()) == Empty()
    assert await FutureMaybe.from_(m).and_then_async(
        lambda _: Future.from_(Some(2))
    ) == Some(2)
    assert (
        await FutureMaybe.from_(m).and_then_async(lambda _: Future.from_(Empty()))
        == Empty()
    )


async def test_empty_and() -> None:
    m = Empty().as_maybe(int)

    assert m.and_(Some(2)) == Empty()
    assert m.and_(Empty()) == Empty()
    assert m.and_then(lambda _: Some(2)) == Empty()
    assert m.and_then(lambda _: Empty()) == Empty()
    assert await m.and_then_async(lambda _: Future.from_(Some(2))) == Empty()
    assert await m.and_then_async(lambda _: Future.from_(Empty())) == Empty()

    assert await FutureMaybe.from_(m).and_(Some(2)) == Empty()
    assert await FutureMaybe.from_(m).and_(Empty()) == Empty()
    assert await FutureMaybe.from_(m).and_then(lambda _: Some(2)) == Empty()
    assert await FutureMaybe.from_(m).and_then(lambda _: Empty()) == Empty()
    assert (
        await FutureMaybe.from_(m).and_then_async(lambda _: Future.from_(Some(2)))
        == Empty()
    )
    assert (
        await FutureMaybe.from_(m).and_then_async(lambda _: Future.from_(Empty()))
        == Empty()
    )


async def test_some_or() -> None:
    m = Some(1).as_maybe()

    assert m.or_(Some(2)) == Some(1)
    assert m.or_(Empty()) == Some(1)
    assert m.or_else(lambda: Some(2)) == Some(1)
    assert m.or_else(lambda: Empty()) == Some(1)
    assert await m.or_else_async(lambda: Future.from_(Some(2))) == Some(1)
    assert await m.or_else_async(lambda: Future.from_(Empty())) == Some(1)

    assert await FutureMaybe.from_(m).or_(Some(2)) == Some(1)
    assert await FutureMaybe.from_(m).or_(Empty()) == Some(1)
    assert await FutureMaybe.from_(m).or_else(lambda: Some(2)) == Some(1)
    assert await FutureMaybe.from_(m).or_else(lambda: Empty()) == Some(1)
    assert await FutureMaybe.from_(m).or_else_async(
        lambda: Future.from_(Some(2))
    ) == Some(1)
    assert await FutureMaybe.from_(m).or_else_async(
        lambda: Future.from_(Empty())
    ) == Some(1)


async def test_empty_or() -> None:
    m = Empty().as_maybe(int)

    assert m.or_(Some(2)) == Some(2)
    assert m.or_(Empty()) == Empty()
    assert m.or_else(lambda: Some(2)) == Some(2)
    assert m.or_else(lambda: Empty()) == Empty()
    assert await m.or_else_async(lambda: Future.from_(Some(2))) == Some(2)
    assert await m.or_else_async(lambda: Future.from_(Empty())) == Empty()

    assert await FutureMaybe.from_(m).or_(Some(2)) == Some(2)
    assert await FutureMaybe.from_(m).or_(Empty()) == Empty()
    assert await FutureMaybe.from_(m).or_else(lambda: Some(2)) == Some(2)
    assert await FutureMaybe.from_(m).or_else(lambda: Empty()) == Empty()
    assert await FutureMaybe.from_(m).or_else_async(
        lambda: Future.from_(Some(2))
    ) == Some(2)
    assert (
        await FutureMaybe.from_(m).or_else_async(lambda: Future.from_(Empty()))
        == Empty()
    )


@pytest.mark.parametrize(
    ("maybe", "target"),
    [
        (Some(1), Some(1)),
        (Some(2), Empty()),
        (Empty(), Empty()),
    ],
)
async def test_filter(maybe: Maybe[int], target: Maybe[int]) -> None:
    assert maybe.filter(lambda x: x % 2 == 1) == target
    assert await maybe.filter_async(lambda x: Future.from_(x % 2 == 1)) == target

    assert await FutureMaybe.from_(maybe).filter(lambda x: x % 2 == 1) == target
    assert (
        await FutureMaybe.from_(maybe).filter_async(lambda x: Future.from_(x % 2 == 1))
        == target
    )


def test_some_ctors() -> None:
    assert Some.from_optional(1) == Some(1)
    assert Some.from_optional(None) == Empty()
    assert Some.from_if(1, lambda x: x % 2 == 1) == Some(1)
    assert Some.from_if(2, lambda x: x % 2 == 1) == Empty()
