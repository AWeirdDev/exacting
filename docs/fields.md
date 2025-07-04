# Fields

Fields in `exacting` are rather pretty straightforward, just as what you'd expect from `dataclasses`.

```python
from exacting import Exact, field

class StoreItem(Exact):
    name: str = field()
    price: int = field()
```

## Min, max

You can check for the minimum/maximum length or value by passing the `minv` or `maxv` parameter.

```python
from exacting import Exact, field

class Sequence(Exact):
    id: str = field(minv=2)  # checks for len()
    some: int = field(maxv=4)  # checks for value
    data: list[int] = field(minv=4, maxv=4)  # len() must be 4


# ✅ OK!
Sequence(
    id="hello",
    some=4,
    data=[1, 2, 3, 4]
)
```

## Regex

`exacting` also has a built-in Regex matching field utility.

```python
from exacting import Exact, field

class Hamburger(Exact):
    name: str = field(regex="^[A-Z]+$")

# ✅ GOOD. Emphasized enough!
Hamburger(name="WHOPPER")

# ❌ ERROR. Can you be louder?
Hamburger(name="bigmac")
```

Note that the `regex` parameter won't work (skipped) if used on field types that aren't `str`.

## Aliases

Aliases are only used when serializing/deserializing.

!!! warning

    We're still working on it... stay tuned, I guess.
