import pytest
from eventsourcing.domain import AggregateEvent

from modules.common.time import get_timestamp
from modules.common.utils import get_path_to_class
from modules.templates.domain.aggregates import TemplateAggregate
from modules.templates.domain.events import (
    TemplateCreated,
    TemplateCompleted,
    TemplateStarted,
)
from .. import fakers


def test_template_created_event(template_aggregate: TemplateAggregate):
    # Given
    event_version = 1
    template_info = fakers.fake_template_info()

    # When
    event = TemplateCreated(
        originator_id=template_aggregate.id,
        originator_version=event_version,
        timestamp=template_aggregate.created_on,
        originator_topic=get_path_to_class(TemplateAggregate),
        info=template_info,
    )

    # Then
    assert isinstance(event, AggregateEvent)
    assert event.originator_id == template_aggregate.id
    assert event.timestamp == template_aggregate.created_on
    assert event.timestamp == template_aggregate.modified_on
    assert event.originator_version == event_version
    assert event.info == template_info


def test_template_created_event_is_immutable():
    # Given
    event = TemplateCreated(
        originator_id=1,
        originator_version=1,
        timestamp=get_timestamp(),
        originator_topic=get_path_to_class(TemplateAggregate),
        info=fakers.fake_template_info(),
    )

    # When / Then
    with pytest.raises(AttributeError):
        event.info = fakers.fake_template_info()


def test_template_started_event(template_aggregate: TemplateAggregate):
    # When
    event = TemplateStarted(
        originator_id=template_aggregate.id,
        originator_version=template_aggregate.version,
        timestamp=template_aggregate.modified_on,
    )

    # Then
    assert isinstance(event, AggregateEvent)
    assert event.originator_id == template_aggregate.id
    assert event.timestamp == template_aggregate.modified_on
    assert event.originator_version == template_aggregate.version


def test_template_started_event_is_immutable(template_aggregate: TemplateAggregate):
    # Given
    event = TemplateStarted(
        originator_id=template_aggregate.id,
        originator_version=template_aggregate.version,
        timestamp=template_aggregate.modified_on,
    )

    # When / Then
    with pytest.raises(AttributeError):
        event.timestamp = get_timestamp()


def test_template_completed_event(template_aggregate: TemplateAggregate):
    # When
    event = TemplateCompleted(
        originator_id=template_aggregate.id,
        originator_version=template_aggregate.version,
        timestamp=template_aggregate.modified_on,
    )

    # Then
    assert isinstance(event, AggregateEvent)
    assert event.originator_id == template_aggregate.id
    assert event.timestamp == template_aggregate.modified_on
    assert event.originator_version == template_aggregate.version


def test_template_completed_event_is_immutable(template_aggregate: TemplateAggregate):
    # Given
    event = TemplateCompleted(
        originator_id=template_aggregate.id,
        originator_version=template_aggregate.version,
        timestamp=template_aggregate.modified_on,
    )

    # When / Then
    with pytest.raises(AttributeError):
        event.timestamp = get_timestamp()
