# Annotated

Annotated types allow you to annotate any value onto the type field.

```python
from typing import Annotated

#         type, metadata.......
Annotated[str,  "any data", 123]
```

`exacting` only checks for the type, not the metadata.

For future development of `exacting`, it might be used as a doc field.

## Validator

The `AnnotatedV` ("Annotated" validator) focuses on the target validator provided in the first parameter, the metadata is not related to the validation and is only stored for later use.

```python
from exacting import AnnotatedV, IntV

va = AnnotatedV(IntV(), ["some", "metadata"])

va.metadata  # list[Any]
va.target  # int (validator)

va.validate(123)  # Ok!
va.validate(1.2)  # ERROR
```
