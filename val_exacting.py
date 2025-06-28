import time
import random
import string
from exacting import Exact, field


def gen_str(length: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


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


def gen_reply():
    return Reply(
        user="@" + gen_str(5),
        content=gen_str(20),
        metadata=Meta(
            liked=random.choice([True, False]),
            flags=[gen_str(3) for _ in range(random.randint(0, 3))],
        ),
    )


def gen_comment():
    return Comment(
        user="@" + gen_str(5),
        stars=random.randint(1, 5),
        body=gen_str(40),
        replies=[gen_reply() for _ in range(random.randint(1, 3))],
    )


def gen_place():
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
