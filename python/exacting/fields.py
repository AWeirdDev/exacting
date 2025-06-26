from typing import Any, Callable, Optional, TypeVar
from dataclasses import field as dataclass_field

from .exacting import Regex
from .etypes import BaseType, TypeResult


class RegexType(BaseType[str]):
    regex: Regex

    def __init__(self, pattern: str):
        self.regex = Regex(pattern)

    def validate(self, x: Any) -> TypeResult[str]:
        if not isinstance(x, str):
            return TypeResult(ok=x)

        if not self.regex.validate(x):
            return TypeResult(
                errors=["Failed to validate Regex on str (doesn't match)"]
            )
        else:
            return TypeResult(ok=x)


T = TypeVar("T")


def field(
    *,
    default: Optional[T] = None,
    default_factory: Optional[Callable[[], T]] = None,
    hash: Optional[bool] = None,
    regex: Optional[str] = None,
    alias: Optional[str] = None,
) -> Any:
    """Creates a field.

    Args:
        default (optional): The default value. Cannot be set at the same time with `default_factory`.
        default_factory (optional): A callable function to create the default value.
            Cannot be set at the same time with `default`.
        hash (bool, optional): Hashable?
        regex (str, optional): Check regex for `str`, if the current field is typed to as a `str`.
        alias (str, optional): Alias for serializing/deserializing, but not used in Python.
    """
    validators = []
    if regex is not None:
        validators.append(RegexType(regex))

    metadata = {"exacting_validators": validators, "exacting_alias": alias}

    if default is not None and default_factory is None:
        return dataclass_field(default=default, hash=hash, metadata=metadata)
    elif default is None and default_factory is not None:
        return dataclass_field(
            default_factory=default_factory, hash=hash, metadata=metadata
        )
    else:
        return dataclass_field(hash=hash, metadata=metadata)
