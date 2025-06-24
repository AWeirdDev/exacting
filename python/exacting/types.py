from dataclasses import Field
from typing import Dict, Protocol


class Dataclass(Protocol):
    __dataclass_fields__: Dict[str, Field]
