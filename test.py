from typing import Literal
from exacting import Exact, field


class Person(Exact):
    name: str | int = field(regex="^[A-Za-z]+$")
    stuff: Literal["a", "b"] = field(default="b")


person = Person(name=123)
d = person.exact_as_bytes()
print(Person.exact_from_bytes(d))
