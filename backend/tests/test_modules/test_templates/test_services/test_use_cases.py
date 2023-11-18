import pytest
from sqlalchemy.orm import Session

from modules.templates.domain.value_objects import TEMPLATE_ID_TYPE, TemplateStatus
from modules.templates.dto import Template as TemplateDto
from modules.templates.services import (
    exceptions,
    create_template,
    get_template,
    get_templates,
    start_template,
    complete_template,
)
from persistence_layer import TemplateReadModel
from .. import fakers


def test_create_template_creates_template(session: Session):
    # Given
    template_info = fakers.fake_template_info()

    # When
    template_id = create_template(
        info=template_info,
    )

    # Then
    assert isinstance(template_id, TEMPLATE_ID_TYPE)
    template = get_template(template_id=template_id)
    assert template_id == template.id
    assert template.status == TemplateStatus.NEW
    assert get_read_model_instance(session=session, template_id=template_id) is not None


def test_start_template_starts_template(
    session: Session, template_environment: TemplateDto
):
    # When
    template = start_template(template_id=template_environment.id)

    # Then
    assert isinstance(template, TemplateDto)
    assert template.status == TemplateStatus.IN_PROGRESS
    assert (
        get_read_model_instance(session=session, template_id=template.id).status
        == TemplateStatus.IN_PROGRESS
    )


def test_start_template_raises_exception_when_specified_id_doesnt_exist(
    session: Session, template_environment: TemplateDto
):
    # When and then
    with pytest.raises(exceptions.TemplateDoesntExist):
        start_template(
            template_id=fakers.fake_template_id(),
        )


def test_start_template_raises_exception_when_specified_id_read_model_doesnt_exist(
    session: Session, template_environment: TemplateDto
):
    # Given
    delete_read_model_instance(session=session, template_id=template_environment.id)

    # When and then
    with pytest.raises(exceptions.TemplateDoesntExist):
        start_template(
            template_id=fakers.fake_template_id(),
        )


def test_complete_template_completes_template(
    session: Session, template_environment: TemplateDto
):
    # Given
    start_template(template_id=template_environment.id)

    # When
    template = complete_template(template_id=template_environment.id)

    # Then
    assert isinstance(template, TemplateDto)
    assert template.status == TemplateStatus.COMPLETED
    assert (
        get_read_model_instance(session=session, template_id=template.id).status
        == TemplateStatus.COMPLETED
    )


def test_complete_template_raises_exception_when_specified_id_doesnt_exist(
    session: Session, template_environment: TemplateDto
):
    # When and then
    with pytest.raises(exceptions.TemplateDoesntExist):
        complete_template(
            template_id=fakers.fake_template_id(),
        )


def test_complete_template_raises_exception_when_specified_id_read_model_doesnt_exist(
    session: Session, template_environment: TemplateDto
):
    # Given
    delete_read_model_instance(session=session, template_id=template_environment.id)

    # When and then
    with pytest.raises(exceptions.TemplateDoesntExist):
        start_template(
            template_id=fakers.fake_template_id(),
        )


def test_get_template_returns_data_when_specified_id_exists(
    template_environment: TemplateDto,
):
    # When
    template = get_template(template_id=template_environment.id)

    # Then
    assert isinstance(template, TemplateDto)


def test_get_template_raises_exception_when_specified_id_doesnt_exist():
    # When and then
    with pytest.raises(exceptions.TemplateDoesntExist):
        get_template(
            template_id=fakers.fake_template_id(),
        )


def test_get_templates_no_results_when_no_records_in_database():
    # When
    results = get_templates()

    # Then
    assert isinstance(results, list)
    assert not results


def test_get_templates_returns_results_when_records_in_database(
    template_environment: TemplateDto,
):
    # When
    results = get_templates()

    # Then
    assert isinstance(results, list)
    assert results


def get_read_model_instance(session: Session, template_id: TEMPLATE_ID_TYPE):
    return session.query(TemplateReadModel).filter_by(id=template_id).first()


def delete_read_model_instance(session: Session, template_id: TEMPLATE_ID_TYPE):
    session.delete(get_read_model_instance(session=session, template_id=template_id))
    session.flush()
