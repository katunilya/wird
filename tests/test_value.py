import inspect
import operator
from typing import Any

from wird import Future, Value


def test_map() -> None:
    val = Value({"x": 0}).map(operator.or_, {"a": 1}).unwrap(as_type=dict[str, int])

    assert val == {"x": 0, "a": 1}


def test_inspect() -> None:
    val = Value({"x": 0}).inspect(operator.setitem, "a", 1).unwrap()

    assert val == {"x": 0, "a": 1}


async def test_map_async() -> None:
    awaitable_val = (
        Value({"x": 0}).map_async(lambda x: Future.from_({**x, "a": 1})).unwrap()
    )

    assert inspect.isawaitable(awaitable_val)

    val = await awaitable_val

    assert val == {"x": 0, "a": 1}


async def test_inspect_async() -> None:
    async def set_item(data: dict, key: Any, value: Any) -> None:
        data[key] = value

    awaitable_val = Value({"x": 0}).inspect_async(set_item, "a", 1).unwrap()

    assert inspect.isawaitable(awaitable_val)

    val = await awaitable_val

    assert val == {"x": 0, "a": 1}
