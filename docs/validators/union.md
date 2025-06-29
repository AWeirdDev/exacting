# Union

The union type allows you to have multiple choices of types.

=== "Python 3.10+"

    ```python
    A | B | C
    ```

=== "Python <= 3.9"

    ```python
    from typing import Union

    Union[A, B, C]
    ```

Union types perform exactly as intended in `exacting`.

## Validator

You can do more than two items for Union by hand, or use an exposed function called `union()` to speed up the process.

```python
from exacting import UnionV, union

# by hand
va = UnionV(StrV(), UnionV(BoolV(), IntV()))

# union()
va = union(StrV(), BoolV(), IntV())

va.a  # str (validator)
va.b  # bool | int (validator)

va.b.a  # bool (validator)
va.b.b  # int (validator)
```
