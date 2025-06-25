from typing import TYPE_CHECKING, Callable, List, Type, TypeVar

import dataclasses
from dataclasses import asdict, dataclass, is_dataclass

from .dc import get_etypes_for_dc

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

    def init(self, *args, **kwargs):
        covered = len(args) + len(kwargs)

        if covered != len(etypes):
            raise ValueError(
                f"(dataclass {dc.__name__!r}) Expected to cover {len(etypes)} parameters, but got {covered}"
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


class Exact:
    """This `Exact` model appends additional functionalities to the current dataclass.

    All the APIs are prefixed with `exact_` to add clarity.
    """

    def __init__(self):
        raise NotImplementedError(
            "The class `Exact` should not be initialized directly, but inherited."
        )

    def exact_as_dict(self):
        """Creates a dictionary representation of this dataclass instance.

        Raises:
            AssertionError: Expected a dataclass
        """
        assert is_dataclass(self)
        return asdict(self)
