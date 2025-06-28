# Exacting

> *(adj.) making great demands on one's skill, attention, or other resources.*

`exacting` is a picky dataclass runtime utility collection, making sure all type annotations are followed.

Essentially... **THE** go-to option for dataclasses. heh.

**🔑 Key features**:

- **100% static typing.** Because I hate nothing too.
- Up to **10x faster** than [`pydantic`](https://pydantic.dev)! (Them: 60ms, us: 6~9ms)

![i aint lying about static typing](https://github.com/user-attachments/assets/875517ff-5dd5-4b63-98fa-e1218ff00627)

## Quick tour

This won't take you long :)

**🛍️ Get `exacting`**:

```haskell
pip install -U exacting
```

**🔥 Define some model**:

(Let's just say you're on Python 3.10+... good boy!)

```python
from exacting import Exact

class Actor(Exact):
    name: str
    portrays: str

class Show(Exact):
    name: str
    description: str | None
    actors: list[Actor]
```

<details>
<summary><b>Nawh... I'm on an older version</b></summary>

Oh, it's definitely okay! We got you covered 🔥🔥

```python
from typing import List, Optional
from exacting import Exact

class Actor(Exact):
    name: str
    portrays: str

class Show(Exact):
    name: str
    description: Optional[str]
    actors: List[Actor]
```

</details>

<br />

**📦 Build 'em**:

```python
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
```

<details>
<summary>🔴 <b>ValidationError: During validation of…</b></summary>


```python
ValidationError:
During validation of dataclass Show at field 'name', got:
  • Expected type <class 'str'>, got <class 'int'>
```

</details>

<br />

Normally, when you use the parameters passed in example (2) above, the Python `dataclasses` library might as well just go with it, because they only put the additional **static typing** to the model, but not at **runtime**. Exacting makes sure that at both times, types are all enforced. It even gives you a detailed error message on where this occurs! (In a cool way)

It's worth noting that error generations are *lazy*, which means once Exacting finds out about a problem about a dataclass, it raises a `ValidationError`. This saves a lot of computation time if you have a larger model.

![praise pydantic](https://github.com/user-attachments/assets/c322bff2-2624-479d-9967-7184580b36c1)

Yeah, we also got fields! Use it like how you'd expect it. Quite literally, lol.

```python
from exacting import Exact, field


def create_ai_slop():
    return "tick tock"

class Comment(Exact):
    user: str = field(regex="^@.+$")
    stars: int = field(minv=1, maxv=5)
    body: str = field(default_factory=create_ai_slop)

# ✅ OK, exacting is HYPED
Comment(
    user="@waltuh",
    stars=5
)

# ❌ Hell nawh, exacting holdin' you at gunpoint
Comment(
    user="ooga booga",  # Regex validation '^@.+$' on str failed
    stars=-1,  # Expected min value of 1, got -1
    body=None  # Expected type <class 'str'>, got <class 'NoneType'>
)
```

Woah! That's a lot of code to process. To put it simply, exacting supports:

- **Regex** validation on `str`
- **Min/max** validation on value (e.g., `int`, `float`) or length (e.g., `str`, `list`)
- **Default** values or factory! Y'know, the old `dataclasses` way, mmmMMM
- This is extra, but **custom** validation! You can make your own if you like

![praise pydantic, exactign sucks](https://github.com/user-attachments/assets/5969c54a-14d0-4023-9f80-b89ae9ea8374)

Kind of, but somehow native performance is way better than Rust. Take a look at this.

