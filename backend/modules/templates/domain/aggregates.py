from uuid import uuid4

from eventsourcing.domain import Aggregate

from .events import TemplateCompleted, TemplateCreated, TemplateStarted
from .exceptions import StatusCantBeChanged
from .value_objects import TemplateInfo, TemplateStatus


"""
Add here code responsible for domain logic and state changes of the aggregate.
"""


class TemplateAggregate(Aggregate):
    def __init__(
        self,
    ):
        self._status: TemplateStatus = None
        self._info: TemplateInfo = None

    @property
    def status(self) -> TemplateStatus:
        return self._status

    @property
    def info(self) -> TemplateInfo:
        return self._info

    @classmethod
    def create(cls, info: TemplateInfo) -> "TemplateAggregate":
        return cls._create(
            event_class=TemplateCreated,
            id=uuid4(),
            info=info,
        )

    def start(self):
        if self._status != TemplateStatus.NEW:
            raise StatusCantBeChanged(
                old_status=self._status.value,
                new_status=TemplateStatus.IN_PROGRESS.value,
            )

        self.trigger_event(
            event_class=TemplateStarted,
        )

    def complete(self):
        if self._status != TemplateStatus.IN_PROGRESS:
            raise StatusCantBeChanged(
                old_status=self._status.value,
                new_status=TemplateStatus.COMPLETED.value,
            )

        self.trigger_event(
            event_class=TemplateCompleted,
        )
