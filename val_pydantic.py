import time
import random
import string
from pydantic import BaseModel, Field
from typing import List, Optional


def gen_str(length: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


class Meta(BaseModel):
    liked: bool
    flags: List[str]


class Reply(BaseModel):
    user: str = Field()
    content: str
    metadata: Meta


class Comment(BaseModel):
    user: str = Field()
    stars: int = Field(..., ge=1, le=5)
    body: Optional[str]
    replies: List[Reply]


class Place(BaseModel):
    name: str
    location: str
    comments: List[Comment]
    metadata: Meta


def gen_reply() -> Reply:
    return Reply(
        user="@" + gen_str(5),
        content=gen_str(20),
        metadata=Meta(
            liked=random.choice([True, False]),
            flags=[gen_str(3) for _ in range(random.randint(0, 3))],
        ),
    )


def gen_comment() -> Comment:
    return Comment(
        user="@" + gen_str(5),
        stars=random.randint(1, 5),
        body=gen_str(40),
        replies=[gen_reply() for _ in range(random.randint(1, 3))],
    )


def gen_place() -> Place:
    return Place(
        name=gen_str(10),
        location=gen_str(20),
        comments=[gen_comment() for _ in range(100)],
        metadata=Meta(liked=True, flags=["safe"]),
    )


start = time.perf_counter()
place = gen_place()
end = time.perf_counter()

print(f"{(end - start) * 1000} ms")
