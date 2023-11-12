from uuid import UUID

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from modules.templates.domain.value_objects import TemplateStatus


Base = declarative_base()


class TemplateReadModel(Base):
    __tablename__ = "template_read_model"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    info: Mapped[dict] = mapped_column(type_=JSON, nullable=False)
    status: Mapped[TemplateStatus] = mapped_column(nullable=False)
