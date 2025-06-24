# exacting
> *(adj.) making great demands on one's skill, attention, or other resources.*

`exacting` is a picky dataclass runtime utility collection, making sure all type annotations are followed.

Yes, **type hints are always on.** No hidden stuff.

## Examples
```python
from exacting import exact

@exact
class Person:
    name: str
    age: int

Person(name="John", age=123)  # Ok!

Person(name="John", age=1.23)
#                       ^^^^
# See the curly underlines? Normally, they pop out 
# from your code editor from the language server, 
# but types aren't strict in **runtime**, which means
# this expression is completely valid if you used 
# @dataclass instead.
# Thankfully, `exacting` gives us an error message:
# 
# TypeError:
# During validation of dataclass Person, a type error occurred: -
# (isinstance) Expected <class 'int'>, got: <class 'float'>
# ...at attribute 'age'
```

Also, you can type anything! (Almost.) Cool.

```python
@exact
class Stuff:
    banana: str | int | bool
    apple: Optional[str]

# ...they all work!
```

***

WIP. More APIs soon.

(c) 2025, AWeirdDev
