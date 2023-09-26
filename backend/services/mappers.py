from persistence_layer import Template as TemplateDb
from .dto import Template as TemplateDto


def map_template_db_to_dto(template_db: TemplateDb) -> TemplateDto:
    return TemplateDto(
        id=template_db.id,
        status=template_db.status,
    )


def map_template_dto_to_db(template_dto: TemplateDto) -> TemplateDb:
    return TemplateDb(
        id=template_dto.id,
        status=template_dto.status,
    )
