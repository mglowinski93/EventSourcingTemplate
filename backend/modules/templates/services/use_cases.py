from persistence_layer import get_session
from .applications import Templates
from .exceptions import (
    TemplateDoesntExist,
    FailedToSaveTemplate,
    FailedToUpdateTemplate,
)
from .mappers import map_template_aggregate_to_template_dto
from ..dto import Template as TemplateDto
from ..domain.value_objects import TEMPLATE_ID_TYPE, TemplateInfo, TemplateStatus
from ..persistence import read_model
from ...common.exceptions import (
    FailedToSaveReadModel,
    FailedToUpdateReadModel,
    ReadModelRecordNotFound,
)


"""
Add here code intended to process a particular business logic of the application.
Actions here must control aggregates and read model state.
"""


templates = Templates()


def create_template(info: TemplateInfo) -> TEMPLATE_ID_TYPE:
    with templates.recorder.transaction() as session:
        template_id = templates.create(info)

        try:
            read_model.save_template(
                session=session,
                template=TemplateDto(
                    id=template_id, info=info, status=TemplateStatus.NEW
                ),
            )
        except FailedToSaveReadModel as err:
            raise FailedToSaveTemplate from err

    return template_id


def start_template(template_id: TEMPLATE_ID_TYPE) -> TemplateDto:
    with templates.recorder.transaction() as session:
        templates.start(template_id)

        try:
            read_model.update_template(
                session=session,
                template_id=template_id,
                status=TemplateStatus.IN_PROGRESS,
            )
        except ReadModelRecordNotFound as err:
            raise TemplateDoesntExist(
                f"Failed to find read model for template with ID: '{template_id}'"
            ) from err
        except FailedToUpdateReadModel as err:
            raise FailedToUpdateTemplate(
                f"Failed to update read model for template with ID: '{template_id}'"
            ) from err

        return map_template_aggregate_to_template_dto(templates.get(template_id))


def complete_template(template_id: TEMPLATE_ID_TYPE) -> TemplateDto:
    with templates.recorder.transaction() as session:
        templates.complete(template_id)

        try:
            read_model.update_template(
                session=session,
                template_id=template_id,
                status=TemplateStatus.COMPLETED,
            )
        except ReadModelRecordNotFound as err:
            raise TemplateDoesntExist(
                f"Failed to find read model for template with ID: '{template_id}'"
            ) from err
        except FailedToUpdateReadModel as err:
            raise FailedToUpdateTemplate(
                f"Failed to update read model for template with ID: '{template_id}'"
            ) from err

        return map_template_aggregate_to_template_dto(templates.get(template_id))


def get_template(template_id: TEMPLATE_ID_TYPE) -> TemplateDto:
    return map_template_aggregate_to_template_dto(templates.get(template_id))


def get_templates() -> list[TemplateDto]:
    with get_session() as session:
        return read_model.get_templates(session)
