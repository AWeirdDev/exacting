from exacting import Exact


class Id(Exact):
    n: int


class Person(Exact):
    name: str
    id: Id


Person(name="asdf", id=Id(n=123))
