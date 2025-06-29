# Literal

Literal types tell `exacting` to check for value equality instead of types.

```python
from typing import Literal

Literal["Hello", b"beep", 123, True]
```

There can be multiple `Literal` items.

Literal types perform exactly as intended in `exacting`.

## Validator

The `LiteralV` ("Literal" validator) checks the equailty of the target values (the "OK" ones) and the provided value.

This validator loops through `self.values` and returns immediately once a match is found.

```python
from exacting import LiteralV

va = LiteralV(["A", 1, True])

va.values # list[Any]

va.validate("A")  # Ok!
va.validate(1)  # Ok!
va.validate(True)  # Ok!
va.validate("B")  # ERROR
```
