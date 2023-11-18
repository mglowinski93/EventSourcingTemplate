from typing import Type

import factory
from uuid import uuid4

from modules.templates.domain.value_objects import TemplateStatus
from modules.templates.persistence.mappers import map_template_info_to_dict
from persistence_layer import TemplateReadModel
from . import fakers


def TemplateReadModelFactory(
    session,
) -> Type[factory.alchemy.SQLAlchemyModelFactory]:
    class _TemplateReadModelFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = TemplateReadModel
            sqlalchemy_session = session
            sqlalchemy_session_persistence = "commit"

        id = factory.LazyFunction(uuid4)
        info = factory.LazyFunction(
            lambda: map_template_info_to_dict(fakers.fake_template_info())
        )
        status = TemplateStatus.NEW

    return _TemplateReadModelFactory
