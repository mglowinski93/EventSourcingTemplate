import pytest

from modules.templates.domain.aggregates import TemplateAggregate, TemplateStatus
from modules.templates.domain.exceptions import StatusCantBeChanged


def test_template_aggregate_start(template_aggregate: TemplateAggregate):
    # Given
    assert template_aggregate.status == TemplateStatus.NEW

    # When
    template_aggregate.start()

    # Then
    assert template_aggregate.status == TemplateStatus.IN_PROGRESS


def test_template_aggregate_cant_be_started_when_already_started(
    template_aggregate: TemplateAggregate,
):
    # Given
    template_aggregate._status = TemplateStatus.IN_PROGRESS

    # When and then
    with pytest.raises(StatusCantBeChanged):
        template_aggregate.start()


def test_template_aggregate_compete(template_aggregate: TemplateAggregate):
    # Given
    template_aggregate._status = TemplateStatus.IN_PROGRESS

    # When
    template_aggregate.complete()

    # Then
    assert template_aggregate.status == TemplateStatus.COMPLETED


def test_template_aggregate_cant_be_completed_when_already_completed(
    template_aggregate: TemplateAggregate,
):
    # Given
    template_aggregate._status = TemplateStatus.COMPLETED

    # When and then
    with pytest.raises(StatusCantBeChanged):
        template_aggregate.complete()


def test_template_aggregate_cant_be_completed_when_not_started(
    template_aggregate: TemplateAggregate,
):
    # Given
    assert template_aggregate.status == TemplateStatus.NEW

    # When and then
    with pytest.raises(StatusCantBeChanged):
        template_aggregate.complete()
