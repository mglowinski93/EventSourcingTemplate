import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.templates.domain.value_objects import TEMPLATE_ID_TYPE
from modules.templates.services import (
    complete_template,
    create_template,
    get_template,
    start_template,
    TemplateDoesntExist,
)
from persistence_layer import TemplateReadModel
from .. import fakers


def test_create_template_returns_template_id(session: Session):
    # Given
    template_info = fakers.fake_template_info()

    # When
    template_id = create_template(
        info=template_info,
    )

    # Then
    assert isinstance(template_id, TEMPLATE_ID_TYPE)
    assert (
        session.scalars(
            select(TemplateReadModel).where(TemplateReadModel.id == template_id)
        ).first()
        is not None
    )


def test_get_template_raises_exception_when_template_doesnt_exist():
    with pytest.raises(TemplateDoesntExist):
        get_template(
            template_id=fakers.fake_template_id(),
        )


def test_start_template_raises_exception_when_template_doesnt_exist():
    with pytest.raises(TemplateDoesntExist):
        start_template(
            template_id=fakers.fake_template_id(),
        )


def test_complete_template_raises_exception_when_template_doesnt_exist():
    with pytest.raises(TemplateDoesntExist):
        complete_template(
            template_id=fakers.fake_template_id(),
        )
