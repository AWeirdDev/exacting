# Any

The `Any` type allows any type to be on the surface, which is generally not a good practice in production.

```python
from typing import Any

Any
```

## Validator

The `AnyV` ("Any" validator) grants every type.

```python
from exacting import AnyV

va = AnyV()
va.validate(123)  # Ok!
va.validate("W")  # Ok!
```
