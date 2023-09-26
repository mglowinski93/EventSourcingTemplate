from dataclasses import dataclass

from persistence_layer import TemplateStatus


@dataclass(frozen=True)
class Template:
    id: int
    status: TemplateStatus
