"""Types for `exacting`.

A variable that's prefixed with `e` followed by a built-in Python type is
inherited from `BaseType`, which supports validation via `validate()`.

The `expect()` function is also available if you'd like to make a custom type.
"""

from dataclasses import is_dataclass
import typing
from typing import Any, Generic, Type, TypeVar

from .types import Dataclass

T = TypeVar("T")
K = TypeVar("K")


def expect(t: Type[T], x: Any) -> T:
    """Expect an instance of a type.

    Args:
        t: The type object.
        x: Any value to test.

    Example:

    ```python
    try:
        expect(str, some_value)
    except TypeError as err:
        print(err.args[0])
    ```

    Raises:
        TypeError: mismatching types.
    """
    if isinstance(x, t):
        return x
    else:
        raise TypeError(f"\n(isinstance) Expected {t}, got: {type(x)}")


class BaseType(Generic[T]):
    def __init__(self): ...
    def validate(self, x: Any) -> T:
        """Validates the type."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return "BaseType"


class StrType(BaseType[str]):
    def validate(self, x: Any) -> str:
        return expect(str, x)

    def __repr__(self) -> str:
        return "str"


estr = StrType()


class IntType(BaseType[int]):
    def validate(self, x: Any) -> int:
        return expect(int, x)

    def __repr__(self) -> str:
        return "int"


eint = IntType()


class BoolType(BaseType[bool]):
    def validate(self, x: Any) -> bool:
        return expect(bool, x)

    def __repr__(self) -> str:
        return "bool"


ebool = BoolType()


class FloatType(BaseType[float]):
    def validate(self, x: Any) -> float:
        return expect(float, x)

    def __repr__(self) -> str:
        return "float"


efloat = FloatType()


class BytesType(BaseType[bytes]):
    def validate(self, x: Any) -> bytes:
        return expect(bytes, x)

    def __repr__(self) -> str:
        return "bytes"


ebytes = BytesType()


class ListType(BaseType[typing.List[T]]):
    target: BaseType[T]

    def __init__(self, target: BaseType[T]):
        self.target = target

    def validate(self, x: Any) -> typing.List[T]:
        x = expect(list, x)

        for idx, item in enumerate(x):
            try:
                x[idx] = self.target.validate(item)
            except TypeError as err:
                message = err.args[0]
                raise TypeError(
                    f"\nDuring validation of list[{self.target!r}], a type error occurred: - {message}\n"
                    f"...at item index {idx}"
                )

        return x

    def __repr__(self) -> str:
        return f"list[{self.target!r}]"


class NoneType(BaseType[None]):
    def validate(self, x: Any) -> None:
        if x is not None:
            raise TypeError(f"\nExpected None, got: {type(x)}")
        return x

    def __repr__(self) -> str:
        return "None"


enone = NoneType()


class AnyType(BaseType[Any]):
    def validate(self, x: Any) -> Any:
        return x


eany = AnyType()


class DictType(BaseType[typing.Dict[K, T]]):
    k_target: BaseType[K]
    v_target: BaseType[T]

    def __init__(self, k_target: BaseType[K], v_target: BaseType[T]):
        self.k_target = k_target
        self.v_target = v_target

    def validate(self, x: Any) -> typing.Dict[K, T]:
        x = expect(dict, x)
        for key, value in x.items():
            try:
                k = self.k_target.validate(key)
            except TypeError as err:
                message = err.args[0]
                raise TypeError(
                    f"\nDuring validation of list[{self.k_target!r}], a type error occurred: - {message}\n"
                    f"...at item key {key!r}"
                )

            try:
                v = self.v_target.validate(value)
            except TypeError as err:
                message = err.args[0]
                raise TypeError(
                    f"\nDuring validation of list[{self.v_target!r}], a type error occurred: - {message}\n"
                    f"...at item key {key!r}"
                )

            x[k] = v

        return x

    def __repr__(self) -> str:
        return f"dict[{self.k_target!r}, {self.v_target!r}]"


class UnionType(BaseType[typing.Union[K, T]]):
    a: BaseType[K]
    b: BaseType[T]

    def __init__(self, a: BaseType[K], b: BaseType[T]):
        self.a = a
        self.b = b

    def validate(self, x: Any) -> typing.Union[K, T]:
        try:
            return self.a.validate(x)
        except TypeError as err:
            message = err.args[0]

        try:
            return self.b.validate(x)
        except TypeError as err:
            raise TypeError(
                f"\nExpected either {self.a!r} or {self.b!r}.\n"
                f"• Attempted {self.a!r}, got: - {message}\n"
                f"• Attempted {self.b!r}, got: - {err.args[0]}"
            )

    def __repr__(self) -> str:
        return f"{self.a!r} | {self.b!r}"


def union(*items: BaseType) -> BaseType:
    """Creates a union type.

    Example:

    ```python
    union(estr, eint, ebool)
    ```
    """
    assert len(items) > 0

    if len(items) > 1:
        return UnionType(items[0], union(*items[1:]))
    else:
        return items[0]


class DataclassType(BaseType[Dataclass]):
    name: str
    target: typing.Dict[str, BaseType]

    def __init__(self, name: str, target: typing.Dict[str, BaseType]):
        self.name = name
        self.target = target

    def validate(self, x: Any) -> Any:
        if not is_dataclass(x):
            raise TypeError(f"Expected dataclass instance, got: {x!r}")

        for name, etype in self.target.items():
            item = getattr(x, name)
            try:
                setattr(x, name, etype.validate(item))
            except TypeError as err:
                raise TypeError(
                    f"\nDuring validation of dataclass {self.name}, a type error occurred: - {err.args[0]}\n"
                    f"...at attribute {name!r}"
                )

        return x

    def __repr__(self) -> str:
        return self.name
