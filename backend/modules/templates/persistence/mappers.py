from modules.templates.domain.value_objects import TemplateInfo, TemplateStatus
from modules.templates.dto import Template as TemplateDto
from persistence_layer import TemplateReadModel as TemplateDb


def map_template_db_read_model_to_dto(template_db: TemplateDb) -> TemplateDto:
    return TemplateDto(
        id=template_db.id,
        info=TemplateInfo(
            value=template_db.info["value"],
        ),
        status=TemplateStatus(template_db.status),
    )


def map_template_dto_to_db_read_model(template_dto: TemplateDto) -> TemplateDb:
    return TemplateDb(
        id=template_dto.id,
        info=map_template_info_to_dict(template_dto.info),
        status=template_dto.status,
    )


def map_template_info_to_dict(template_info: TemplateInfo) -> dict:
    return {
        "value": template_info.value,
    }
