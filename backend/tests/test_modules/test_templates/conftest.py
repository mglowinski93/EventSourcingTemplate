import pytest

from persistence_layer import get_session
from . import fakers


@pytest.fixture
def session():
    with get_session() as session:
        yield session


@pytest.fixture
def template_aggregate():
    yield fakers.fake_template_aggregate()
