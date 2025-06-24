from typing import TYPE_CHECKING, Callable, Type, TypeVar

import dataclasses
from dataclasses import asdict, dataclass, is_dataclass

from .dc import get_etypes_for_dc

T = TypeVar("T", bound=Type)


def get_exact_init(dc: Type) -> Callable:
    etypes = get_etypes_for_dc(dc)

    def init(self, *args, **kwargs):
        if args:
            keys_map = list(etypes)  # keys
            for idx, value in enumerate(args):
                k = keys_map[idx]
                try:
                    v = etypes[keys_map[idx]].validate(value)
                except TypeError as err:
                    raise TypeError(
                        f"\nDuring validation of dataclass {dc.__name__}, a type error occurred: - {err.args[0]}\n"
                        f"...at attribute {k!r}"
                    )
                setattr(self, k, v)

            for key, value in kwargs.items():
                try:
                    setattr(self, key, etypes[key].validate(value))
                except TypeError as err:
                    raise TypeError(
                        f"\nDuring validation of dataclass {dc.__name__}, a type error occurred: - {err.args[0]}\n"
                        f"...at attribute {key!r}"
                    )

        else:
            for key, value in kwargs.items():
                try:
                    setattr(self, key, etypes[key].validate(value))
                except TypeError as err:
                    raise TypeError(
                        f"\nDuring validation of dataclass {dc.__name__}, a type error occurred: - {err.args[0]}\n"
                        f"...at attribute {key!r}"
                    )

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
