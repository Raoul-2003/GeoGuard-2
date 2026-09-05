import uuid
from datetime import datetime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime

Base = declarative_base()

class SoftDeleteMixin:
    """Mixin to add soft delete fields to a model."""
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
