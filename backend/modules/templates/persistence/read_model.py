from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from persistence_layer import TemplateReadModel
from .mappers import (
    map_template_db_read_model_to_dto,
    map_template_dto_to_db_read_model,
)
from ..domain.value_objects import TEMPLATE_ID_TYPE, TemplateStatus
from ..dto import Template as TemplateDto
from ...common.exceptions import (
    FailedToSaveReadModel,
    ReadModelRecordNotFound,
    FailedToUpdateReadModel,
)


"""
Add here code responsible for operations on read model.
Read model in EventSourcing context is a projection of the state of the system
and is used to query the state of the system.
Read model should be updated in response to events.
"""


def get_templates(session: Session) -> list[TemplateDto]:
    return [
        map_template_db_read_model_to_dto(template)
        for template in session.execute(select(TemplateReadModel)).scalars().all()
    ]


def save_template(session: Session, template: TemplateDto):
    session.add(map_template_dto_to_db_read_model(template))
    try:
        session.flush()
    except IntegrityError as err:
        raise FailedToSaveReadModel(message=str(err)) from err


def update_template(
    session: Session, template_id: TEMPLATE_ID_TYPE, status: TemplateStatus
) -> TemplateDto:
    try:
        template_record = (
            session.scalars(
                select(TemplateReadModel).where(TemplateReadModel.id == template_id)
            )
        ).one()
    except NoResultFound as err:
        raise ReadModelRecordNotFound(message=str(err)) from err

    setattr(template_record, "status", status)

    try:
        session.flush()
    except IntegrityError as err:
        raise FailedToUpdateReadModel(message=str(err)) from err

    return map_template_db_read_model_to_dto(template_record)
