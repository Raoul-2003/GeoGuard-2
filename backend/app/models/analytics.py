import uuid
from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from .base import Base, SoftDeleteMixin

class AiModel(Base, SoftDeleteMixin):
    __tablename__ = "ai_models"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False)
    model_type: Mapped[str] = mapped_column(String, nullable=False)
    accuracy: Mapped[float] = mapped_column(Float, nullable=True)
    training_date: Mapped[date] = mapped_column(Date, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True)

class AiAnalysis(Base, SoftDeleteMixin):
    __tablename__ = "ai_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("monitoring_zones.id"), nullable=False)
    image_before_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("satellite_images.id"), nullable=True)
    image_after_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("satellite_images.id"), nullable=False)
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_models.id"), nullable=False)
    
    analysis_type: Mapped[str] = mapped_column(String, nullable=False) # e.g. changement, déforestation
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    processing_time: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String, default="completed")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    results: Mapped[list["ChangeDetectionResult"]] = relationship("ChangeDetectionResult", back_populates="analysis")

class ChangeDetectionResult(Base):
    __tablename__ = "change_detection_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_analyses.id"), nullable=False)
    
    total_pixels: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_pixels: Mapped[int] = mapped_column(Integer, nullable=False)
    change_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    
    geometry = mapped_column(Geometry('POLYGON', srid=4326), nullable=True, index=True)
    surface_ha: Mapped[float] = mapped_column(Float, nullable=False)

    analysis: Mapped["AiAnalysis"] = relationship("AiAnalysis", back_populates="results")
