from dataclasses import dataclass
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
    experiences: list[Experience]


Person(
    name="John",
    age=123,
    experiences=[Experience(title=b"WHEN I POOPPED OFF", years=123)],
)
