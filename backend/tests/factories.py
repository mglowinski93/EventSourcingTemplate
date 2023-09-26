import random
from typing import Optional

import faker

from persistence_layer import TemplateStatus
from services.dto import Template


fake = faker.Faker()


def fake_template_id() -> int:
    return fake.pyint(min_value=0)


def fake_template_status(exclude: Optional[TemplateStatus] = None) -> TemplateStatus:
    return random.choice([key for key in TemplateStatus if key != exclude])


def fake_template() -> Template:
    return Template(
        id=fake_template_id(),
        status=fake_template_status(),
    )
