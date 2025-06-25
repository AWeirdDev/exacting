from typing import TYPE_CHECKING, Callable, List, Type, TypeVar
from typing_extensions import Self, dataclass_transform

import dataclasses
from dataclasses import asdict, dataclass, is_dataclass

from .dc import get_etypes_for_dc
from .exacting import json as ejson  # type: ignore

T = TypeVar("T", bound=Type)


def get_exact_error_message(errors: List[str]) -> str:
    text = "\n"
    indents = 0
    for error in errors:
        if error == "indent":
            indents += 2
            text += " " * indents
            continue
        elif error == "unindent":
            indents -= 2
            text += " " * indents
            continue

        text += f"{error}\n{' ' * indents}"

    return text.rstrip()


def get_exact_init(dc: Type) -> Callable:
    etypes = get_etypes_for_dc(dc)
    dc.__exact_types__ = etypes

    def init(self, *args, **kwargs):
        covered = len(args) + len(kwargs)

        if covered != len(etypes):
            raise ValueError(
                f"(dataclass {dc.__name__!r}) Expected to cover {len(etypes)} parameter(s), but got {covered}"
            )

        if args:
            keys_map = list(etypes)  # keys

            for idx, value in enumerate(args):
                k = keys_map[idx]
                res = etypes[keys_map[idx]].validate(value)
                if res.has_error():
                    raise TypeError(
                        get_exact_error_message(
                            [
                                f"During validation of dataclass {dc.__name__!r} at attribute {k!r}, a type error occurred:",
                                *res.errors,
                            ]
                        )
                    )
                setattr(self, k, res.ok)

            for key, value in kwargs.items():
                res = etypes[key].validate(value)
                if res.has_error():
                    raise TypeError(
                        get_exact_error_message(
                            [
                                f"During validation of dataclass {dc.__name__!r} at attribute {key!r}, a type error occurred:",
                                *res.errors,
                            ]
                        )
                    )
                setattr(self, key, res.ok)

        else:
            for key, value in kwargs.items():
                res = etypes[key].validate(value)
                if res.has_error():
                    raise TypeError(
                        get_exact_error_message(
                            [
                                f"During validation of dataclass {dc.__name__!r} at attribute {key!r}, a type error occurred:",
                                *res.errors,
                            ]
                        )
                    )
                setattr(self, key, res.ok)

        return None  # required!

    return init


def _patch():
    original = dataclasses.dataclass

    def new(item=None, **kwargs):
        if item is None:

            def wrapper(t):
                x = original(t)
                init = get_exact_init(x)
                setattr(x, "__init__", init)
                return x

            return wrapper
        else:
            x = dataclass(item)
            init = get_exact_init(x)
            setattr(x, "__init__", init)
            return x

    return new


# sneaky trick
if TYPE_CHECKING:
    exact = dataclasses.dataclass
else:
    exact = _patch()


@dataclass_transform()
class _ModelKwOnly: ...


class Exact(_ModelKwOnly):
    """
    All the APIs are prefixed with `exact_` to add clarity.
    """

    def __init_subclass__(cls) -> None:
        setattr(cls, "__init__", get_exact_init(dataclass(cls)))

    def exact_as_dict(self):
        """(exacting) Creates a dictionary representation of this dataclass instance.

        Raises:
            AssertionError: Expected a dataclass
        """
        assert is_dataclass(self)
        return asdict(self)

    @classmethod
    def exact_from_json(cls, raw: str, *, strict: bool = True) -> Self:
        """(exacting) Initialize this dataclass model from JSON.

        When `strict` is set to `False`, exacting uses JSON5, allowing comments,
        trailing commas, object keys without quotes, single quoted strings and more.

        Example:

        ```python
        class Person(Exact):
            name: str
            age: int

        # strict mode (default)
        Person.exact_from_json(\"\"\"
        {
            "name": "Harry",
            "age": 23
        }
        \"\"\")

        # lenient :)
        Person.exact_from_json(\"\"\"
        {
            /*
                hell yeah!
            */
            name: "Walter",
            age: 23, // <- trailing commas? yeah!
        }
        \"\"\", strict=False)
        ```

        Args:
            raw (str): The raw JSON.
            strict (bool): Whether to use strict mode.
        """
        if strict:
            data = ejson.json_to_py(raw)
        else:
            data = ejson.jsonc_to_py(raw)

        return cls(**data)
