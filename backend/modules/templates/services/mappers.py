from ..domain.aggregates import TemplateAggregate
from ..dto import Template as TemplateDto


def map_template_aggregate_to_template_dto(
    template_aggregate: TemplateAggregate,
) -> TemplateDto:
    return TemplateDto(
        id=template_aggregate.id,
        info=template_aggregate.info,
        status=template_aggregate.status,
    )
