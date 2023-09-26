import pytest
from sqlalchemy.future import select

from persistence_layer import Template as TemplateDb, get_session
from services import (
    get_template,
    save_template,
    TemplateDoesntExist,
)
from services.mappers import map_template_dto_to_db
from .. import factories


def test_get_template_raises_exception_when_template_doesnt_exist():
    with pytest.raises(TemplateDoesntExist):
        get_template(
            template_id=factories.fake_template_id(),
        )


def test_get_template_returns_template_when_template_exist():
    # Given
    faked_template = factories.fake_template()
    with get_session() as session:
        session.add(map_template_dto_to_db(faked_template))

    # When
    template = get_template(
        template_id=faked_template.id,
    )

    # Then
    assert faked_template == template


def test_save_template_saves_template():
    # Given
    template = factories.fake_template()

    # When
    save_template(
        template=template,
    )

    # Then
    with get_session() as session:
        assert (
            session.scalars(
                select(TemplateDb).where(TemplateDb.id == template.id)
            )
        ).first() is not None
