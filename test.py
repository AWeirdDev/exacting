from typing import Annotated, Literal
from exacting import Exact, unsafe


class Comment(Exact):
    user: str
    title: str
    stars: int
    body: str | None = None


class Place(Exact):
    name: str
    location: str
    comments: list[Comment]


with unsafe():
    d = Place.__unsafe_init__(
        name="McDonald's",
        location="McDonald's Rd.",
        comments=[Comment.__unsafe_init__(user="Waltuh", title="ITBOY", stars=2)],
    ).exact_as_dict()
print(Place.exact_from_dict(d))
