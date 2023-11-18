import pytest

from modules.templates.domain.aggregates import TemplateAggregate, TemplateStatus
from modules.templates.domain.value_objects import TEMPLATE_ID_TYPE
from modules.templates.services import TemplateDoesntExist
from modules.templates.services.applications import Templates as TemplateApplication

from .. import fakers


def test_template_application_create_creates_aggregate(
    template_application: TemplateApplication,
):
    # Given
    template_info = fakers.fake_template_info()

    # When
    template_id = template_application.create(template_info)

    # Then
    assert isinstance(template_id, TEMPLATE_ID_TYPE)
    assert isinstance(
        template_application.repository.get(template_id), TemplateAggregate
    )


def test_template_application_start_starts_aggregate(
    template_aggregate: TemplateAggregate, template_application: TemplateApplication
):
    # Given
    template_application.save(template_aggregate)

    # When
    result = template_application.start(template_aggregate.id)

    # Then
    assert result is None
    assert (
        template_application.repository.get(template_aggregate.id).status
        == TemplateStatus.IN_PROGRESS
    )


def test_template_application_start_raises_exception_when_no_aggregate_found(
    template_application: TemplateApplication,
):
    # When and then
    with pytest.raises(TemplateDoesntExist):
        template_application.start(fakers.fake_template_id())


def test_template_application_complete_completes_aggregate(
    template_aggregate: TemplateAggregate, template_application: TemplateApplication
):
    # Given
    template_aggregate.start()
    template_application.save(template_aggregate)

    # When
    result = template_application.complete(template_aggregate.id)

    # Then
    assert result is None
    assert (
        template_application.repository.get(template_aggregate.id).status
        == TemplateStatus.COMPLETED
    )


def test_template_application_complete_raises_exception_when_no_aggregate_found(
    template_application: TemplateApplication,
):
    # When and then
    with pytest.raises(TemplateDoesntExist):
        template_application.complete(fakers.fake_template_id())


def test_template_application_get_returns_aggregate(
    template_aggregate: TemplateAggregate, template_application: TemplateApplication
):
    # Given
    template_application.save(template_aggregate)

    # When
    retrieved_aggregate = template_application.get(template_aggregate.id)

    # Then
    assert retrieved_aggregate == template_aggregate


def test_template_application_get_raises_exception_when_no_aggregate_found(
    template_application: TemplateApplication,
):
    # When and then
    with pytest.raises(TemplateDoesntExist):
        template_application.get(fakers.fake_template_id())
