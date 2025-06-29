# Native types

Most native types are instantly available! These are all the available types:

```python
str
int
float
bool
bytes
list[...]
dict[..., ...]
```

You probably noticed that `tuple` or `set` isn't available. Yes, currently.


## Validators

For non-container-like types:

```python
from exacting import (
    StrV, 
    IntV, 
    FloatV, 
    BoolV, 
    BytesV
)
```

For container-like types:

```python
from exacting import ListV, DictV

lva = ListV(StrV())  # list[str] (validator)
dva = ListV(StrV(), StrV())  # dict[str, str] (validator)
```
