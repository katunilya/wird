import operator

import pytest

from wird import Err, ErrUnwrapError, Future, FutureResult, Ok, OkUnwrapError, Result


async def test_ok_unwraps() -> None:
    r = Ok(1).of_err_type(str)

    assert r.unwrap() == 1
    assert r.unwrap_or(2) == 1
    assert r.unwrap_or_else(lambda: 2) == 1
    assert await r.unwrap_or_else_async(lambda: Future.from_(2)) == 1

    with pytest.raises(OkUnwrapError, match="expected Err, got Ok"):
        r.unwrap_err()

    with pytest.raises(OkUnwrapError, match="on ok"):
        r.unwrap_err(on_ok="on ok")

    assert r.unwrap_err_or("err") == "err"
    assert r.unwrap_err_or_else(lambda: "err") == "err"
    assert await r.unwrap_err_or_else_async(lambda: Future.from_("err")) == "err"

    assert await FutureResult.from_(r).unwrap() == 1
    assert await FutureResult.from_(r).unwrap_or(2) == 1
    assert await FutureResult.from_(r).unwrap_or_else(lambda: 2) == 1
    assert (
        await FutureResult.from_(r).unwrap_or_else_async(lambda: Future.from_(2)) == 1
    )

    with pytest.raises(OkUnwrapError, match="expected Err, got Ok"):
        await FutureResult.from_(r).unwrap_err()

    with pytest.raises(OkUnwrapError, match="on ok"):
        await FutureResult.from_(r).unwrap_err(on_ok="on ok")

    assert await FutureResult.from_(r).unwrap_err_or("err") == "err"
    assert await FutureResult.from_(r).unwrap_err_or_else(lambda: "err") == "err"
    assert (
        await FutureResult.from_(r).unwrap_err_or_else_async(
            lambda: Future.from_("err")
        )
        == "err"
    )


async def test_err_unwraps() -> None:
    r = Err("err").of_ok_type(int)

    with pytest.raises(ErrUnwrapError, match="expected Ok, got Err"):
        r.unwrap()

    with pytest.raises(ErrUnwrapError, match="on err"):
        r.unwrap(on_err="on err")

    assert r.unwrap_or(2) == 2
    assert r.unwrap_or_else(lambda: 2) == 2
    assert await r.unwrap_or_else_async(lambda: Future.from_(2)) == 2

    assert r.unwrap_err() == "err"
    assert r.unwrap_err_or("error") == "err"
    assert r.unwrap_err_or_else(lambda: "error") == "err"
    assert await r.unwrap_err_or_else_async(lambda: Future.from_("error")) == "err"

    with pytest.raises(ErrUnwrapError, match="expected Ok, got Err"):
        await FutureResult.from_(r).unwrap()

    with pytest.raises(ErrUnwrapError, match="on err"):
        await FutureResult.from_(r).unwrap(on_err="on err")

    assert await FutureResult.from_(r).unwrap_or(2) == 2
    assert await FutureResult.from_(r).unwrap_or_else(lambda: 2) == 2
    assert (
        await FutureResult.from_(r).unwrap_or_else_async(lambda: Future.from_(2)) == 2
    )

    assert await FutureResult.from_(r).unwrap_err() == "err"
    assert await FutureResult.from_(r).unwrap_err_or("error") == "err"
    assert await FutureResult.from_(r).unwrap_err_or_else(lambda: "error") == "err"
    assert (
        await FutureResult.from_(r).unwrap_err_or_else_async(
            lambda: Future.from_("error")
        )
        == "err"
    )


@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), Ok(5)),
        (Err(""), Err("")),
    ],
)
async def test_result_map(
    result: Result[int, str],
    target: Result[int, str],
) -> None:
    assert (
        await result.map(operator.add, 1)
        .map_async(lambda x: Future.from_(x + 1))
        .map(operator.add, 1)
        .map_async(lambda x: Future.from_(x + 1))
        == target
    )


@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(""), Ok("")),
        (Err(1), Err(5)),
    ],
)
async def test_result_map_err(
    result: Result[str, int],
    target: Result[str, int],
) -> None:
    assert (
        await result.map_err(operator.add, 1)
        .map_err_async(lambda x: Future.from_(x + 1))
        .map_err(operator.add, 1)
        .map_err_async(lambda x: Future.from_(x + 1))
        == target
    )


@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok({}), Ok({"a": 1, "b": 2, "c": 3, "d": 4})),
        (Err(""), Err("")),
    ],
)
async def test_result_inspect(
    result: Result[dict, str],
    target: Result[dict, str],
) -> None:
    async def set_item(data: dict, key: str, value: int) -> None:
        data[key] = value

    assert (
        await result.inspect(operator.setitem, "a", 1)
        .inspect_async(set_item, "b", 2)
        .inspect(operator.setitem, "c", 3)
        .inspect_async(set_item, "d", 4)
    )


@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Err({}), Err({"a": 1, "b": 2, "c": 3, "d": 4})),
        (Ok(""), Ok("")),
    ],
)
async def test_result_inspect_err(
    result: Result[str, dict],
    target: Result[str, dict],
) -> None:
    async def set_item(data: dict, key: str, value: int) -> None:
        data[key] = value

    assert (
        await result.inspect_err(operator.setitem, "a", 1)
        .inspect_err_async(set_item, "b", 2)
        .inspect_err(operator.setitem, "c", 3)
        .inspect_err_async(set_item, "d", 4)
    ) == target


async def test_ok_predicates() -> None:
    r = Ok(1).of_err_type(str)

    assert r.is_ok()
    assert r.is_ok_and(lambda x: x % 2 == 1)
    assert r.is_ok_or(lambda x: len(x) > 10)
    assert await r.is_ok_and_async(lambda x: Future.from_(x % 2 == 1))
    assert await r.is_ok_or_async(lambda x: Future.from_(len(x) > 10))

    assert not r.is_err()
    assert not r.is_err_and(lambda x: len(x) > 10)
    assert r.is_err_or(lambda x: x % 2 == 1)
    assert not await r.is_err_and_async(lambda x: Future.from_(len(x) > 10))
    assert await r.is_err_or_async(lambda x: Future.from_(x % 2 == 1))

    assert await FutureResult.from_(r).is_ok()
    assert await FutureResult.from_(r).is_ok_and(lambda x: x % 2 == 1)
    assert await FutureResult.from_(r).is_ok_or(lambda x: len(x) > 10)
    assert await FutureResult.from_(r).is_ok_and_async(
        lambda x: Future.from_(x % 2 == 1)
    )
    assert await FutureResult.from_(r).is_ok_or_async(
        lambda x: Future.from_(len(x) > 10)
    )

    assert not await FutureResult.from_(r).is_err()
    assert not await FutureResult.from_(r).is_err_and(lambda x: len(x) > 10)
    assert await FutureResult.from_(r).is_err_or(lambda x: x % 2 == 1)
    assert not await FutureResult.from_(r).is_err_and_async(
        lambda x: Future.from_(len(x) > 10)
    )
    assert await FutureResult.from_(r).is_err_or_async(
        lambda x: Future.from_(x % 2 == 1)
    )


async def test_err_predicates() -> None:
    r = Err(1).of_ok_type(str)

    assert not r.is_ok()
    assert not r.is_ok_and(lambda x: len(x) > 10)
    assert r.is_ok_or(lambda x: x % 2 == 1)
    assert not await r.is_ok_and_async(lambda x: Future.from_(len(x) > 10))
    assert await r.is_ok_or_async(lambda x: Future.from_(x % 2 == 1))

    assert r.is_err()
    assert r.is_err_and(lambda x: x % 2 == 1)
    assert r.is_err_or(lambda x: len(x) > 10)
    assert await r.is_err_and_async(lambda x: Future.from_(x % 2 == 1))
    assert await r.is_err_or_async(lambda x: Future.from_(len(x) > 10))

    assert not await FutureResult.from_(r).is_ok()
    assert not await FutureResult.from_(r).is_ok_and(lambda x: len(x) > 10)
    assert await FutureResult.from_(r).is_ok_or(lambda x: x % 2 == 1)
    assert not await FutureResult.from_(r).is_ok_and_async(
        lambda x: Future.from_(len(x) > 10)
    )
    assert await FutureResult.from_(r).is_ok_or_async(
        lambda x: Future.from_(x % 2 == 1)
    )

    assert await FutureResult.from_(r).is_err()
    assert await FutureResult.from_(r).is_err_and(lambda x: x % 2 == 1)
    assert await FutureResult.from_(r).is_err_or(lambda x: len(x) > 10)
    assert await FutureResult.from_(r).is_err_and_async(
        lambda x: Future.from_(x % 2 == 1)
    )
    assert await FutureResult.from_(r).is_err_or_async(
        lambda x: Future.from_(len(x) > 10)
    )


async def test_ok_and() -> None:
    r = Ok(1).of_err_type(str)

    assert r.and_(Ok(2)) == Ok(2)
    assert r.and_(Err("")) == Err("")
    assert r.and_then(lambda _: Ok(2)) == Ok(2)
    assert r.and_then(lambda _: Err("")) == Err("")
    assert await r.and_then_async(lambda _: Future.from_(Ok(2))) == Ok(2)
    assert await r.and_then_async(lambda _: Future.from_(Err(""))) == Err("")

    assert await FutureResult.from_(r).and_(Ok(2)) == Ok(2)
    assert await FutureResult.from_(r).and_(Err("")) == Err("")
    assert await FutureResult.from_(r).and_then(lambda _: Ok(2)) == Ok(2)
    assert await FutureResult.from_(r).and_then(lambda _: Err("")) == Err("")
    assert await FutureResult.from_(r).and_then_async(
        lambda _: Future.from_(Ok(2))
    ) == Ok(2)
    assert await FutureResult.from_(r).and_then_async(
        lambda _: Future.from_(Err(""))
    ) == Err("")


async def test_ok_or() -> None:
    r = Ok(1).of_err_type(str)

    assert r.or_(Ok(2)) == Ok(1)
    assert r.or_(Err("")) == Ok(1)
    assert r.or_else(lambda _: Ok(2)) == Ok(1)
    assert r.or_else(lambda _: Err("")) == Ok(1)
    assert await r.or_else_async(lambda _: Future.from_(Ok(2))) == Ok(1)
    assert await r.or_else_async(lambda _: Future.from_(Err(""))) == Ok(1)

    assert await FutureResult.from_(r).or_(Ok(2)) == Ok(1)
    assert await FutureResult.from_(r).or_(Err("")) == Ok(1)
    assert await FutureResult.from_(r).or_else(lambda _: Ok(2)) == Ok(1)
    assert await FutureResult.from_(r).or_else(lambda _: Err("")) == Ok(1)
    assert await FutureResult.from_(r).or_else_async(
        lambda _: Future.from_(Ok(2))
    ) == Ok(1)
    assert await FutureResult.from_(r).or_else_async(
        lambda _: Future.from_(Err(""))
    ) == Ok(1)


async def test_err_and() -> None:
    r = Err(1).of_ok_type(str)

    assert r.and_(Ok("ok")) == Err(1)
    assert r.and_(Err(2)) == Err(1)
    assert r.and_then(lambda _: Ok("ok")) == Err(1)
    assert r.and_then(lambda _: Err(2)) == Err(1)
    assert await r.and_then_async(lambda _: Future.from_(Ok("ok"))) == Err(1)
    assert await r.and_then_async(lambda _: Future.from_(Err(2))) == Err(1)

    assert await FutureResult.from_(r).and_(Ok("ok")) == Err(1)
    assert await FutureResult.from_(r).and_(Err(2)) == Err(1)
    assert await FutureResult.from_(r).and_then(lambda _: Ok("ok")) == Err(1)
    assert await FutureResult.from_(r).and_then(lambda _: Err(2)) == Err(1)
    assert await FutureResult.from_(r).and_then_async(
        lambda _: Future.from_(Ok("ok"))
    ) == Err(1)
    assert await FutureResult.from_(r).and_then_async(
        lambda _: Future.from_(Err(2))
    ) == Err(1)


async def test_err_or() -> None:
    r = Err(1).of_ok_type(str)

    assert r.or_(Ok("ok")) == Ok("ok")
    assert r.or_(Err(2)) == Err(2)
    assert r.or_else(lambda _: Ok("ok")) == Ok("ok")
    assert r.or_else(lambda _: Err(2)) == Err(2)
    assert await r.or_else_async(lambda _: Future.from_(Ok("ok"))) == Ok("ok")
    assert await r.or_else_async(lambda _: Future.from_(Err(2))) == Err(2)

    assert await FutureResult.from_(r).or_(Ok("ok")) == Ok("ok")
    assert await FutureResult.from_(r).or_(Err(2)) == Err(2)
    assert await FutureResult.from_(r).or_else(lambda _: Ok("ok")) == Ok("ok")
    assert await FutureResult.from_(r).or_else(lambda _: Err(2)) == Err(2)
    assert await FutureResult.from_(r).or_else_async(
        lambda _: Future.from_(Ok("ok"))
    ) == Ok("ok")
    assert await FutureResult.from_(r).or_else_async(
        lambda _: Future.from_(Err(2))
    ) == Err(2)
