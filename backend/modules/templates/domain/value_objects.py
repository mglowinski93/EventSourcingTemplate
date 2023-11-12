from dataclasses import dataclass
from enum import Enum, unique
from uuid import UUID


TEMPLATE_ID_TYPE = UUID


@unique
class TemplateStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


@dataclass(frozen=True)
class TemplateInfo:
    value: str
