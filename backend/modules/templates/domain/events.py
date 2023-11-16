from eventsourcing.domain import AggregateCreated, AggregateEvent

from .value_objects import TemplateInfo, TemplateStatus


"""
Add here code defining events that are used to change the state of the aggregate and
actions that happens in response to the events (apply methods in particular event).
"""


class TemplateCreated(AggregateCreated):
    info: TemplateInfo


class TemplateStarted(AggregateEvent):
    def apply(self, aggregate: "TemplateAggregate"):
        aggregate._status = TemplateStatus.IN_PROGRESS


class TemplateCompleted(AggregateEvent):
    def apply(self, aggregate: "TemplateAggregate"):
        aggregate._status = TemplateStatus.COMPLETED
