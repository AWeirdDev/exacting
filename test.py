from dataclasses import dataclass
from exacting.validator_map import get_dc_validator


@dataclass
class Person:
    name: str


print(get_dc_validator(Person).validate(Person(name="123")))
