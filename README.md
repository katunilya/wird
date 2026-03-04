# wird

`wird` is a library that provides basic monads in python. Core idea is to provide
mechanics for writing purely python pipeline-styled code.

> **Why wird?** Wird is a misspelling of Anglo-Saxon / Old North word "wyrd". It means
> fate, but not totally predefined, more like a consequence of previous deeds.

## Pipelines

Before getting into `wird` API it's worth explaining concept of pipeline-styled code.
Mainly our code is imperative - we describe what we do to achieve some result in steps,
one by one. It's not worth to reject imperative code in favor of declarative one (where
we describe the result instead of steps for getting it), as most languages are generally
imperative and it's more convenient to provide better ways to write it.

Different languages provide pipelines in different forms. For example in C# or Java it
is provided with so called Fluent API (sometimes method chaining). Example:

```csharp
int[] numbers = [ 5, 10, 8, 3, 6, 12 ];

IEnumerable<int> evenNumbersSorted = numbers
    .Where(num => num % 2 == 0)
    .OrderBy(num => num);
```

There we write some class that allows us to chain method execution in order to perform
some action. This is quite nice approach, however it's not really extensible and does
not suit to most of the business cases where we want to separate bits of logic into
different entities.

Mostly this kind of syntax is used for builder pattern:

```csharp
var host = new WebHostBuilder() 
    .UseKestrel() 
    .UseContentRoot(Directory.GetCurrentDirectory()) 
    .UseStartup<Startup>() 
    .Build(); 

host.Run(); 
```

In functional languages you can find so called "pipe operator" - `|>`. Let's take a look
at simple case - we want to put to square some number, that convert that to string and
reverse it. In F# you might write that like:

```fsharp
let result = rev (toStr (square 512))
```

Problem of this piece of code is that despite or algorithm is simple and direct, when we
write code it steps are written in reverse order and we need to "unwrap" function calls.

With pipe operator same code becomes much more elegant:

```fsharp
let result = 512
    |> square
    |> toStr
    |> rev
```

All actions are written one-by-one in the same order as they executed. This is much more
readable code.

Basically `wird` is written to provide this mechanic to python language in some
opinionated form inspired by Rust language.

## Monads

### `Value`

Container for sync value that provides pipe-styled execution of arbitrary functions.
Let's look at the example:

```python
import operator

from wird import Value


res = (
    Value(3)
    .map(operator.add, 1)       # 3 + 1 -> 4
    .map(operator.mul, 3)       # 4 * 3 -> 12
    .map(operator.truediv, 2)   # 12 / 2 -> 6
    .inspect(print)             # print 6.0 & pass next
    .unwrap(as_type=int)        # extract 6.0 from container
)
```

`Value` is a simple wrapper around passed value with special methods (`map` /
`map_async` / `inspect` / `inspect_async`) that bind passed function to container value
(read as invoke / apply). Thus it is basically is a simplest monad.

`Value` provides the following interface:

- `Value.unwrap` - method for extracting internally stored value with optional type
  casting (only for type checker, not actual casting happens)
- `Value.map` - binding method for sync functions
- `Value.map_async` - binding method for async functions
- `Value.inspect` - binding method for sync side-effect functions
- `Value.inspect_async` - binding method for async side-effect functions

Main different between `map` and `inspect` is that `map` wraps the result of the
executed function into `Value` container and `inspect` just invokes function passing
stored value next. If stored value is mutable, `inspect` can be used to modify it via
side effect.

### `Future`

Container for async values. It is similar to `Value` and provides nearly the same
interface. When we invoke any of async methods in `Value` we actually return `Future`
container, as now stored value is computed asynchronously and requires `await`.

```python
import operator

from wird import Value

async def mul_async(x: int, y: int) -> int:
  return x * y

async def truediv_async(x: int, y: int) -> float:
  return x / y

async def main():
  res = await (
    Value(3)
    .map(operator.add, 1)         # 3 + 1 -> 4 (Value)
    .map_async(mul_async, 3)      # 4 * 3 -> 12 (Future)
    .map_async(truediv_async, 2)  # 12 / 2 -> 6.0 (Future)
    .inspect(print)               # print 6.0 & pass next (Future)
    .unwrap()                     # extract awaitable 6.0 from container
  )

if __name__ == "__main__":
  import asyncio
  asyncio.run(main())
```

`Future` provides the following interface:

- `Future.unwrap` - extract internally stored awaitable value
- `Future.map` - binding method for sync functions
- `Future.map_async` - binding method for async functions
- `Future.inspect` - binding method for sync side-effect functions
- `Future.inspect_async` - binding method for async side-effect functions
- `Future.from_` - static method for creating awaitable object from sync value

Also `Future` is awaitable by itself, so one can just await `Future` itself instead of
calling `Future.unwrap`, but to stay uniform it is recommended to use `Future.unwrap`.

### `Maybe`

Despite `Value` and `Future`, `Maybe` is not a single container, but rather a pair of
containers - `Some` and `Empty`. Each resembles additional property of data - its
presence.

`Some` indicates that data is present allowing it to be processed. `Empty` on the other
hand marks that there is not data and we can't perform execution ignoring that.
Basically it hides explicit `is None` checks, taking it as internal rule of function
mapping.

Possible relevant case of usage is database patch / update operations, when we
intentionally want to provide some abstract interface that allows optional column
update. For example we store in SQL database following data structure:

```python
from dataclasses import dataclass
from datetime import date


@dataclass
class Customer:
  uid: int
  first_name: str
  second_name: str
  birthdate: date | None = None
```

We provide HTTP route to update this entity in DB. If we've provided a field in request
body, then this field must be updated. Commonly one will make each field in DTO (except
for ID) optional with default `None` value, but what to do with `birthdate`? When
parsing we will propagate default `None` so we do not know if this `None` was passed
explicitly or we've implicitly set it via DTO default.

`Maybe` allows to explicitly separate this cases, allowing us to have `None` as present value:

```python
from dataclasses import dataclass
from datetime import date

from wird import Empty, Maybe


@dataclass
class CustomerUpdate:
  uid: int
  first_name: Maybe[str] = Empty()
  second_name: Maybe[str] = Empty()
  birthdate: Maybe[date | None] = Empty()
```

Thus when `birthdate` is `Empty` we know that we do not have to update this column at
all, and when it is `Some` we can safely set `None` as desired value.

`Maybe` provides the following interface:

- `Maybe.unwrap` - extract internally stored value on `Some`, raise `EmptyUnwrapError`
  on `Empty`
- `Maybe.unwrap_or` - extract internally stored value on `Some` or return passed
  replacement value on `Empty`
- `Maybe.unwrap_or_none` - extract internally stored value on `Some` or return `None`
  on `Empty`
- `Maybe.unwrap_or_else` - extract internally stored value on `Some` or return result of
  execution of factory function for replacement value on `Empty`
- `Maybe.unwrap_or_else_async` - same as `Maybe.unwrap_or_else`, but for async factory
  function
- `Maybe.map` - binding method for sync functions, applies only on `Some`
- `Maybe.map_async` - same as `Maybe.map`, but for async functions
- `Maybe.inspect` - binding method for sync side-effect functions, applies only on
  `Some`
- `Maybe.inspect_async` - same as `Maybe.inspect`, but for async functions
- `Maybe.and_` - logical AND for 2 `Maybe` values, replaces self `Maybe` with passed
  `Maybe` if first one is `Some`
- `Maybe.and_then` - same as `Maybe.map`, but for sync functions that return `Maybe`
- `Maybe.and_then_async` - same as `Maybe.and_then`, but for async functions
- `Maybe.or_` - logical OR for 2 `Maybe` values, replaces self `Maybe` with passed
  `Maybe` if first one is `Empty`
- `Maybe.or_else` - replaces `Empty` with `Maybe` result of passed sync function
- `Maybe.or_else_async` - same as `Maybe.or_else`, but for async functions
- `Maybe.is_some` - `True` on `Some` container
- `Maybe.is_some_and` - `True` on `Some` container and passed predicate being `True`
- `Maybe.is_some_and_async` - same as `Maybe.is_some_and`, but for async predicates
- `Maybe.is_empty` - `True` on `Empty` container
- `Maybe.is_empty_or` - `True` on `Empty` container or passed predicate being `True`
- `Maybe.is_empty_or_async` - same as `Maybe.is_empty_or`, but for async predicates
- `Maybe.filter` - if predicate is `False` replaces `Maybe` with `Empty`
- `Maybe.filter_async` - same as `Maybe.filter`, but for async predicates

In order to provide seamless experience, instead of making developer to work with
`Future[Maybe[T]]` we provide `FutureMaybe` container that provides exactly the same
interface as sync `Maybe`. Worth noting that `FutureMaybe` is awaitable, like `Future`,
and returns internally stored `Maybe` instance.

Also in some cases one might need point-free versions of `Maybe` interface methods, so
one can access them via `maybe` module.
