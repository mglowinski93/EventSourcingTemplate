from enum import Enum

from sqlalchemy.orm import Mapped, declarative_base, mapped_column


Base = declarative_base()


class TemplateStatus(str, Enum):
    NEW = "NEW"
    COMPLETED = "COMPLETED"


class Template(Base):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[TemplateStatus] = mapped_column(nullable=False)
