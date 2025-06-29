# Unsafe

If you take a closer look at a model inherited from the `Exact` model, there's a `__unsafe_init__()` function which allows you to skip all type checks.

However, if directly called, you'd get an error:

```python
from exacting import Exact

class Person(Exact):
    name: str

Person.__unsafe_init__(name="Walter")
```

??? failure "RuntimeError: Scope is not in unsafe()…"

    ```python
    RuntimeError: Scope is not in unsafe(), canceled operation
    ```
