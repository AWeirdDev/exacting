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


