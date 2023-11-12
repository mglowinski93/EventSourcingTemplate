from dataclasses import dataclass

from modules.templates.domain.value_objects import (
    TEMPLATE_ID_TYPE,
    TemplateInfo,
    TemplateStatus,
)


@dataclass(frozen=True)
class Template:
    id: TEMPLATE_ID_TYPE
    info: TemplateInfo
    status: TemplateStatus
