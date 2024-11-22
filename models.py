from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry
from datetime import datetime

table_registry = registry()


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
