from exacting import Exact


class Actor(Exact):
    name: str
    portrays: str


class Show(Exact):
    name: str
    description: str | None
    actors: list[Actor]

# (1) ✅ OK, exacting is happi
Show(
    name="Severance",
    description="great show",
    actors=[
        Actor(name="Adam Scott", portrays="Mark S."),
        Actor(name="Britt Lower", portrays="Helly R."),
    ]
)

# (2) ❌ Nuh-uh, exacting is angri
Show(
    name=123,
    description=False,
    actors=[
        "Walter White",
        "Jesse Pinkman"
    ]
)