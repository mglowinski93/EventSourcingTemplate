import random
from uuid import uuid4
from typing import Optional

import faker

from modules.templates.domain.aggregates import TemplateAggregate
from modules.templates.domain.value_objects import (
    TEMPLATE_ID_TYPE,
    TemplateInfo,
    TemplateStatus,
)
from modules.templates.dto import Template


fake = faker.Faker()


def fake_template_id() -> TEMPLATE_ID_TYPE:
    return uuid4()


def fake_template_status(exclude: Optional[TemplateStatus] = None) -> TemplateStatus:
    return random.choice([key for key in TemplateStatus if key != exclude])


def fake_template_info() -> TemplateInfo:
    return TemplateInfo(value=fake.pystr(min_chars=1, max_chars=100))


def fake_template_aggregate() -> TemplateAggregate:
    return TemplateAggregate.create(
        info=fake_template_info(),
    )


def fake_template() -> Template:
    return Template(
        id=fake_template_id(),
        status=fake_template_status(),
    )
