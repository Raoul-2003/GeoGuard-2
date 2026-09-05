import uuid
from datetime import datetime
from sqlalchemy import String, Float, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from .base import Base, SoftDeleteMixin
import enum

class AlertSeverity(str, enum.Enum):
    LOW = "faible"
    MEDIUM = "moyen"
    HIGH = "élevé"
    CRITICAL = "critique"

class AlertStatus(str, enum.Enum):
    NEW = "nouvelle"
    VALIDATION = "validation"
    CONFIRMED = "confirmée"
    REJECTED = "rejetée"
    CLOSED = "clôturée"

class Alert(Base, SoftDeleteMixin):
    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("monitoring_zones.id"), nullable=False)
    analysis_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_analyses.id"), nullable=False)
    
    type: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[AlertSeverity] = mapped_column(Enum(AlertSeverity), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[AlertStatus] = mapped_column(Enum(AlertStatus), default=AlertStatus.NEW)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    missions: Mapped[list["FieldMission"]] = relationship("FieldMission", back_populates="alert")

class MissionStatus(str, enum.Enum):
    CREATED = "créée"
    ASSIGNED = "assignée"
    TRAVELING = "en déplacement"
    INSPECTING = "inspection"
    COMPLETED = "terminée"

class FieldMission(Base, SoftDeleteMixin):
    __tablename__ = "field_missions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("alerts.id"), nullable=False)
    assigned_user: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    priority: Mapped[str] = mapped_column(String, nullable=False)
    location = mapped_column(Geometry('POINT', srid=4326), nullable=False, index=True)
    status: Mapped[MissionStatus] = mapped_column(Enum(MissionStatus), default=MissionStatus.CREATED)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    alert: Mapped["Alert"] = relationship("Alert", back_populates="missions")
    evidences: Mapped[list["FieldEvidence"]] = relationship("FieldEvidence", back_populates="mission")

class FieldEvidence(Base):
    __tablename__ = "field_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("field_missions.id"), nullable=False)
    
    type: Mapped[str] = mapped_column(String, nullable=False) # photo, vidéo, document
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    gps = mapped_column(Geometry('POINT', srid=4326), nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    mission: Mapped["FieldMission"] = relationship("FieldMission", back_populates="evidences")

class Report(Base, SoftDeleteMixin):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String, nullable=False) # exécutif, scientifique
    zone_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("monitoring_zones.id"), nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
