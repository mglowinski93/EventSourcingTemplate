import pytest
from sqlalchemy.orm import Session

from modules.common.exceptions import ReadModelRecordNotFound
from modules.templates.dto import Template as TemplateDto
from modules.templates.persistence.read_model import (
    get_templates,
    save_template,
    update_template,
)
from persistence_layer import TemplateReadModel
from .. import factories, fakers


def test_get_templates_returns_no_results_when_no_records_in_database(session: Session):
    # When
    results = get_templates(session)

    # Then
    assert isinstance(results, list)
    assert not results


def test_get_templates_returns_results_when_records_in_database(
    session: Session, template_read_model_factory: factories.TemplateReadModelFactory
):
    # Given
    template = template_read_model_factory()

    # When
    results = get_templates(session)

    # Then
    assert isinstance(results, list)
    assert results
    assert all(isinstance(result, TemplateDto) for result in results)
    assert results[0].id == template.id


def test_save_templates_creates_record_in_database(
    session: Session,
):
    # Given
    template = fakers.fake_template_dto()

    # When
    results = save_template(session=session, template=template)

    # Then
    assert results is None
    assert (
        session.query(TemplateReadModel).filter_by(id=template.id).first() is not None
    )


def test_update_templates_updates_record_in_database(
    session: Session, template_read_model_factory: factories.TemplateReadModelFactory
):
    # Given
    template = template_read_model_factory()
    new_status = fakers.fake_template_status(exclude=template.status)

    # When
    results = update_template(
        session=session, template_id=template.id, status=new_status
    )

    # Then
    assert isinstance(results, TemplateDto)
    assert results.status == new_status


def test_template_application_complete_raises_exception_when_no_record_found(
    session: Session,
):
    # When and then
    with pytest.raises(ReadModelRecordNotFound):
        update_template(
            session=session,
            template_id=fakers.fake_template_id(),
            status=fakers.fake_template_status(),
        )
