from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.future import select

from persistence_layer import Template as TemplateDb, get_session
from .dto import Template as TemplateDto
from .exceptions import FailedToSaveTemplate, TemplateDoesntExist
from .mappers import map_template_db_to_dto, map_template_dto_to_db


def save_template(template: TemplateDto):
    with get_session() as session:
        session.add(map_template_dto_to_db(template))
        try:
            session.flush()
        except IntegrityError as err:
            raise FailedToSaveTemplate(message=str(err)) from err


def get_template(template_id: int) -> TemplateDto:
    with get_session() as session:
        try:
            return map_template_db_to_dto(
                (
                    session.scalars(
                        select(TemplateDb).where(TemplateDb.id == template_id)
                    )
                ).one()
            )
        except NoResultFound as err:
            raise TemplateDoesntExist(template_id) from err
