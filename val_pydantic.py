import time
import random
import string
from pydantic import BaseModel, Field
from typing import List, Optional


def gen_str(length: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


class MetaP(BaseModel):
    liked: bool
    flags: List[str]


class ReplyP(BaseModel):
    user: str = Field()
    content: str
    metadata: MetaP


class CommentP(BaseModel):
    user: str = Field()
    stars: int = Field(..., ge=1, le=5)
    body: Optional[str]
    replies: List[ReplyP]


class PlaceP(BaseModel):
    name: str
    location: str
    comments: List[CommentP]
    metadata: MetaP


def gen_reply() -> ReplyP:
    return ReplyP(
        user="@" + gen_str(5),
        content=gen_str(20),
        metadata=MetaP(
            liked=random.choice([True, False]),
            flags=[gen_str(3) for _ in range(random.randint(0, 3))],
        ),
    )


def gen_comment() -> CommentP:
    return CommentP(
        user="@" + gen_str(5),
        stars=random.randint(1, 5),
        body=gen_str(40),
        replies=[gen_reply() for _ in range(random.randint(1, 3))],
    )


def gen_place() -> PlaceP:
    return PlaceP(
        name=gen_str(10),
        location=gen_str(20),
        comments=[gen_comment() for _ in range(100)],
        metadata=MetaP(liked=True, flags=["safe"]),
    )


start = time.perf_counter()
for i in range(10):
    gen_place()
end = time.perf_counter()

print(f"{(end - start) * 1000} ms")

from exacting import Exact, field


class Meta(Exact):
    liked: bool = field()
    flags: list[str] = field()


class Reply(Exact):
    user: str = field()
    content: str = field()
    metadata: Meta


class Comment(Exact):
    user: str = field()
    stars: int = field(minv=1, maxv=5)
    body: str | None
    replies: list[Reply]


class Place(Exact):
    name: str
    location: str
    comments: list[Comment]
    metadata: Meta


def gen_reply2():
    return Reply(
        user="@" + gen_str(5),
        content=gen_str(20),
        metadata=Meta(
            liked=random.choice([True, False]),
            flags=[gen_str(3) for _ in range(random.randint(0, 3))],
        ),
    )


def gen_comment2():
    return Comment(
        user="@" + gen_str(5),
        stars=random.randint(1, 5),
        body=gen_str(40),
        replies=[gen_reply2() for _ in range(random.randint(1, 3))],
    )


def gen_place2():
    return Place(
        name=gen_str(10),
        location=gen_str(20),
        comments=[gen_comment2() for _ in range(100)],
        metadata=Meta(liked=True, flags=["safe"]),
    )


start = time.perf_counter()
for i in range(10):
    gen_place2()
end = time.perf_counter()

print(f"{(end - start) * 1000} ms")
