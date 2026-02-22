import operator

from wird import Future


async def test_map() -> None:
    val = await (
        Future.from_({"x": 0})
        .map(operator.or_, {"a": 1})
        .unwrap(as_type=dict[str, int])
    )

    assert val == {"x": 0, "a": 1}


async def test_inspect() -> None:
    val = await Future.from_({"x": 0}).inspect(operator.setitem, "a", 1).unwrap()

    assert val == {"x": 0, "a": 1}


async def test_map_async() -> None:
    val = await (
        Future.from_({"x": 0}).map_async(lambda x: Future.from_({**x, "a": 1})).unwrap()
    )

    assert val == {"x": 0, "a": 1}


async def test_inspect_async() -> None:
    async def set_item(data, key, value) -> None:
        data[key] = value

    val = await Future.from_({"x": 0}).inspect_async(set_item, "a", 1).unwrap()

    assert val == {"x": 0, "a": 1}


async def test_await() -> None:
    assert await Future.from_(1) == await Future.from_(1).unwrap()
