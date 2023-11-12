from modules.templates.domain.value_objects import TemplateInfo, TemplateStatus
from modules.templates.dto import Template as TemplateDto
from persistence_layer import TemplateReadModel as TemplateDb


def map_template_db_read_model_to_dto(template_db: TemplateDb) -> TemplateDto:
    return TemplateDto(
        id=template_db.id,
        info=TemplateInfo(
            value=TemplateStatus(template_db.info["value"]),
        ),
        status=template_db.status,
    )


def map_template_dto_to_db_read_model(template_dto: TemplateDto) -> TemplateDb:
    return TemplateDb(
        id=template_dto.id,
        info={
            "value": template_dto.info.value,
        },
        status=template_dto.status,
    )
