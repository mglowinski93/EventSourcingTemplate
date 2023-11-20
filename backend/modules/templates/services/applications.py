from eventsourcing.application import AggregateNotFound
from eventsourcing.persistence import Transcoder, Transcoding

from persistence_layer import PersistentEventApplication
from ..domain.value_objects import TEMPLATE_ID_TYPE, TemplateInfo
from ..domain.aggregates import TemplateAggregate
from .exceptions import TemplateDoesntExist


"""
Add code here that mediates between the use-cases and aggregate.
This layer is added to manage persistence of the events (that is the aggregate state).
"""


class TemplateInfoTranscoder(Transcoding):
    type = TemplateInfo
    name = "template_info"

    def encode(self, obj: TemplateInfo) -> dict:
        return {
            "value": obj.value,
        }

    def decode(self, data: dict) -> TemplateInfo:
        return TemplateInfo(
            value=data["value"],
        )


# Application class should be named after the subdomain that its domain model supports,
# or the bounded context that its domain model constitutes.
class Templates(PersistentEventApplication):
    def register_transcodings(self, transcoder: Transcoder):
        super().register_transcodings(transcoder)
        transcoder.register(TemplateInfoTranscoder())

    def create(self, value: TemplateInfo) -> TEMPLATE_ID_TYPE:
        template = TemplateAggregate.create(value)
        self.save(template)

        return template.id

    def start(self, template_id: TEMPLATE_ID_TYPE):
        try:
            template = self.repository.get(template_id)
        except AggregateNotFound as err:
            raise TemplateDoesntExist(
                f"Failed to find aggregate for template with ID: '{template_id}'"
            ) from err

        template.start()
        self.save(template)

    def complete(self, template_id):
        try:
            template = self.repository.get(template_id)
        except AggregateNotFound as err:
            raise TemplateDoesntExist(
                f"Failed to recreate aggregate for template with ID: '{template_id}'"
            ) from err

        template.complete()
        self.save(template)

    def get(self, template_id) -> TemplateAggregate:
        try:
            return self.repository.get(template_id)
        except AggregateNotFound as err:
            raise TemplateDoesntExist(
                f"Failed to recreate aggregate for template with ID: '{template_id}'"
            ) from err
