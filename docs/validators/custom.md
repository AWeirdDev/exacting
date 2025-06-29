# Custom

!!! warning "Under construction"

    The full API documentation is not yet complete :(


Yup. Starting from `v0.2.0`, the custom validator API gets a little more easy on your eyes.

Let's say we want to make a custom type that checks if the integers of a list are all divisible by 5.

```python
from exacting import Validator, Result, ListV, IntV

list_of_int = ListV(IntV())

class CoolListV(Validator):
    """My cool list validator :)"""

    def validate(self, value, **options) -> Result:
        # It must be a list of integers!
        res: Result = list_of_int.validate(value)
        if not res.is_ok():
            # not a list
            return res

        the_list = res.unwrap()
        for item in the_list:
            if item % 5 != 0:
                return Result.Err("Not divisible by 5")

        return Result.Ok(the_list)
```

Then, try it out:

```python
va = CoolListV()
result = va.validate([10, 20, 30])
result.raise_for_err()  # no error!

assert result.unwrap() == [10, 20, 30]
```

Or use it on an `Exact` model:

```python
from typing import Any
from exacting import Exact, field

class Numbers(Exact):
    # for demo, we'll use Any for now to show 
    # the validator's work
    array: Any = field(validators=[CoolListV()])

Numbers(array=[100])  # Ok!
Numbers(array=[123])  # ERROR
```
