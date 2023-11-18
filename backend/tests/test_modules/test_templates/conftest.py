import pytest
from sqlalchemy.orm import Session

from modules.templates.domain.aggregates import TemplateAggregate
from modules.templates.dto import Template as TemplateDto
from modules.templates.services import use_cases
from modules.templates.services.applications import Templates as TemplateApplication
from persistence_layer import TemplateReadModel, get_session
from . import fakers, factories


@pytest.fixture
def session() -> Session:
    with get_session() as session:
        yield session
        session.query(TemplateReadModel).delete()


@pytest.fixture
def template_aggregate() -> TemplateAggregate:
    yield fakers.fake_template_aggregate()


@pytest.fixture
def template_application() -> TemplateApplication:
    yield fakers.fake_template_application()


@pytest.fixture
def template_read_model_factory(
    session: Session,
) -> type[factories.TemplateReadModelFactory]:
    return factories.TemplateReadModelFactory(session)


@pytest.fixture
def template_environment(
    session: Session,
    template_application: TemplateApplication,
    template_read_model_factory: type[factories.TemplateReadModelFactory],
) -> TemplateDto:
    template_id = use_cases.create_template(fakers.fake_template_info())
    return use_cases.get_template(template_id=template_id)
