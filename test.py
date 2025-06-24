from typing import Optional
from exacting import Exact, exact


@exact
class Experience(Exact):
    title: str
    years: Optional[int] = None


@exact
class Person(Exact):
    name: str
    age: int


Person(name="John", age=123).exact_as_dict()
