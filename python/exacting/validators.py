from abc import ABC
from dataclasses import is_dataclass
from typing import Any, Dict, List, Type, TypeVar
from weakref import ReferenceType

from .types import DataclassType, Result, indexable

T = TypeVar("T")


def expect(typ: Type[T], on: Any) -> Result[T]:
    """Expect a type instance on a value."""
    if not isinstance(on, typ):
        return Result.Err(f"Expected type {typ!r}, got {type(on)}")

    return Result.Ok(on)


class Validator(ABC):
    def validate(self, value: Any, **options) -> Result: ...


class IntV(Validator):
    def validate(self, value: Any, **options) -> "Result[int]":
        return expect(int, value)

    def __repr__(self) -> str:
        return "int"


class FloatV(Validator):
    def validate(self, value: Any, **options) -> "Result[float]":
        return expect(float, value)

    def __repr__(self) -> str:
        return "float"


class BoolV(Validator):
    def validate(self, value: Any, **options) -> "Result[bool]":
        return expect(bool, value)

    def __repr__(self) -> str:
        return "bool"


class StrV(Validator):
    def validate(self, value: Any, **options) -> "Result[str]":
        return expect(str, value)

    def __repr__(self) -> str:
        return "str"


class BytesV(Validator):
    def validate(self, value: Any, **options) -> "Result[bytes]":
        return expect(bytes, value)

    def __repr__(self) -> str:
        return "bytes"


class ListV(Validator):
    target: Validator

    def __init__(self, target: Validator):
        self.target = target

    def validate(self, value: Any, **options) -> "Result":
        res = expect(list, value)
        if not res.is_ok():
            return res

        array = res.unwrap()
        for idx, item in enumerate(array):
            item_res = self.target.validate(item, **options)
            if not item_res.is_ok():
                return item_res.trace(
                    f"During validation of {self!r}, a validation error occurred:"
                )

            array[idx] = item_res.unwrap()

        return Result.Ok(array)

    def __repr__(self) -> str:
        return f"list[{self.target!r}]"


class DictV(Validator):
    key: Validator
    value: Validator

    def __init__(self, key: Validator, value: Validator):
        self.key = key
        self.value = value

    def validate(self, value: Any, **options) -> "Result":
        res = expect(dict, value)
        if not res.is_ok():
            return res

        hashmap = res.unwrap()
        for k, v in list(hashmap.items()):
            k_res = self.key.validate(k, **options)
            if not k_res.is_ok():
                return k_res.trace(
                    f"During validation of {self!r}, the literal key value {k!r} failed to validate:"
                )

            kk = k_res.unwrap()

            v_res = self.value.validate(v, **options)
            if not v_res.is_ok():
                return v_res.trace(
                    f"During validation of {self!r}, the *value* paired to key {k!r} failed to validate:"
                )

            vv = v_res.unwrap()

            del hashmap[k]
            hashmap[kk] = vv

        return Result.Ok(hashmap)

    def __repr__(self) -> str:
        return f"dict[{self.key!r}, {self.value!r}]"


class UnionV(Validator):
    a: Validator
    b: Validator

    def __init__(self, a: Validator, b: Validator):
        self.a = a
        self.b = b

    def validate(self, value: Any, **options) -> "Result":
        a_res = self.a.validate(value, **options)
        if a_res.is_ok():
            return a_res

        b_res = self.b.validate(value, **options)
        if b_res.is_ok():
            return b_res

        return Result.trace_below(
            f"Failed to validate {self!r}, tried variant A and B, got errors:",
            *a_res.unwrap_err(),
            *b_res.unwrap_err(),
        )

    def __repr__(self) -> str:
        return f"{self.a!r} | {self.b!r}"


class AnyV(Validator):
    def validate(self, value: Any, **options) -> Result:
        return Result.Ok(value)

    def __repr__(self) -> str:
        return "Any"


class NoneV(Validator):
    def validate(self, value: Any, **options) -> Result:
        if value is not None:
            return Result.Err("Expected None")
        else:
            return Result.Ok(value)


class LiteralV(Validator):
    values: List[Any]

    def __init__(self, values: "List[Any]"):
        self.values = values

    def validate(self, value: Any, **options) -> Result:
        for item in self.values:
            if value == item:
                return Result.Ok(value)

        return Result.Err(f"Failed to validate on {self!r}: no eq match")

    def __repr__(self) -> str:
        return f"Literal[{', '.join(self.values)}]"


class AnnotatedV(Validator):
    target: Validator
    metadata: List[Any]

    def __init__(self, target: Validator, metadata: List[Any]):
        self.target = target
        self.metadata = metadata

    def validate(self, value: Any, **options) -> Result:
        return self.target.validate(value, **options)

    def __repr__(self) -> str:
        return f"Annotated[{self.target}, ...metadata]"


class DataclassV(Validator):
    targets: Dict[str, Validator]
    rf: ReferenceType["DataclassType"]

    def __init__(self, dc_rf: ReferenceType, targets: Dict[str, Validator]):
        self.rf = dc_rf
        self.targets = targets

    def validate(self, value: Any, **options) -> Result:
        dc = self.rf()
        if dc is None:
            return Result.Err("(internal) Weakref missing for dataclass")

        if options.get("from_dict"):
            res = expect(dict, value)
            if not res.is_ok():
                return res.trace(f"Expected a dict on dataclass ({self!r}) from_dict:")
            value = res.unwrap()
            data = indexable(value)
        else:
            if not is_dataclass(value):
                return Result.Err(f"Expected a dataclass ({self!r}), got {type(value)}")

            data = indexable(value)

        for field in dc.__dataclass_fields__.values():
            name = field.name
            field_res = self.targets[name].validate(data[name])
            if not field_res.is_ok():
                return field_res.trace(f"During validation of dataclass {self!r}, got:")

            data[name] = field_res.unwrap()

        if options.get("from_dict"):
            result = getattr(dc, "__unsafe_init__")(**data.as_dict())
        else:
            result = data.as_dc()

        return Result.Ok(result)

    def __repr__(self):
        dc = self.rf()
        if dc is None:
            raise RuntimeError("Weakref is gone")
        return repr(dc)
