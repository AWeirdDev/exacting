import dataclasses as std_dc

from collections import deque
from typing import Any, Dict, Generic, Optional, Protocol, Type, TypeVar, Union

T = TypeVar("T")


class Result(Generic[T]):
    """Represents a result."""

    ok_data: Optional[T]
    errors: Optional["deque[str]"]  # O(1)

    def __init__(self, okd: Optional[T], errors: Optional["deque[str]"]):
        self.ok_data = okd
        self.errors = errors

    @classmethod
    def Ok(cls, data: T) -> "Result[T]":
        return cls(data, None)

    @classmethod
    def Err(cls, *errors: str) -> "Result[T]":
        return cls(None, deque(errors))

    def unwrap(self) -> T:
        """Unwrap the OK data."""
        # cheap operation lmfao
        return self.ok_data  # type: ignore

    def unwrap_err(self) -> "deque[str]":
        """Unwrap the Err data."""
        # AGAIN. lmfao! you gotta be responsible.
        return self.errors  # type: ignore

    def is_ok(self) -> bool:
        """CALL."""
        return not self.errors

    def trace(self, upper: str) -> "Result[T]":
        if self.errors is not None:
            self.errors.appendleft("indent")
            self.errors.appendleft(upper)
            self.errors.append("unindent")

        return self

    @classmethod
    def trace_below(cls, upper: str, *items: str) -> "Result[T]":
        errors = deque(items)
        errors.appendleft("indent")
        errors.appendleft(upper)
        errors.append("unindent")

        return cls(okd=None, errors=errors)

    def __repr__(self) -> str:
        if self.is_ok():
            return f"Result.Ok({self.unwrap()!r})"
        else:
            return f"Result.Err({self.unwrap_err()!r})"


class Dataclass(Protocol):
    __dataclass_fields__: Dict[str, std_dc.Field]


DataclassType = Union[Type[Dataclass], Any]


class _Indexable:
    def __getitem__(self, k: str): ...
    def __setitem__(self, k: str, data: Any): ...
    def as_dict(self) -> dict: ...
    def as_dc(self) -> Dataclass: ...


class _DefinitelyDict(_Indexable):
    def __init__(self, d: Dict):
        self.data = d

    def __getitem__(self, k: str):
        self.data[k]

    def __setitem__(self, k: str, data: Any):
        self.data[k] = data

    def as_dict(self) -> dict:
        return self.data

    def as_dc(self) -> Dataclass:
        raise TypeError("This indexable is not a dataclass but a dict")


class _DefinitelyDataclass(_Indexable):
    def __init__(self, dc: Dataclass):
        self.dc = dc

    def __getitem__(self, k: str):
        return getattr(self.dc, k)

    def __setitem__(self, k: str, data: Any):
        setattr(self.dc, k, data)

    def as_dict(self):
        raise TypeError("This indexable is not a dict but a dataclass")

    def as_dc(self) -> Dataclass:
        return self.dc


def indexable(item: Any) -> "_Indexable":
    if isinstance(item, dict):
        return _DefinitelyDict(item)
    else:
        return _DefinitelyDataclass(item)
