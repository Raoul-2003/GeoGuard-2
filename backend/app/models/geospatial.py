import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, Text, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from .base import Base, SoftDeleteMixin
import enum

class ZoneType(str, enum.Enum):
    FOREST = "forêt"
    PARK = "parc"
    URBAN = "urbain"
    AGRICULTURAL = "agricole"
    INDUSTRIAL = "industriel"
    RESERVE = "réserve"

class MonitoringZone(Base, SoftDeleteMixin):
    __tablename__ = "monitoring_zones"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[ZoneType] = mapped_column(Enum(ZoneType), nullable=False)
    geometry = mapped_column(Geometry('POLYGON', srid=4326), nullable=False, index=True)
    area_ha: Mapped[float] = mapped_column(Float, nullable=False)
    protection_level: Mapped[str] = mapped_column(String, nullable=True)
    risk_score: Mapped[float] = mapped_column(Float, nullable=True)
    monitoring_status: Mapped[str] = mapped_column(String, default="active")
    
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    images: Mapped[list["SatelliteImage"]] = relationship("SatelliteImage", back_populates="zone")

class Satellite(Base, SoftDeleteMixin):
    __tablename__ = "satellites"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False) # e.g. Sentinel-2
    provider: Mapped[str] = mapped_column(String, nullable=False)
    resolution: Mapped[float] = mapped_column(Float, nullable=False)
    sensor_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True)

class ImageStatus(str, enum.Enum):
    RECEIVED = "reçue"
    PREPROCESSING = "prétraitement"
    READY_FOR_AI = "prête IA"
    ANALYZED = "analysée"
    ARCHIVED = "archivée"

class SatelliteImage(Base, SoftDeleteMixin):
    __tablename__ = "satellite_images"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    satellite_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("satellites.id"), nullable=False)
    zone_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("monitoring_zones.id"), nullable=False)
    
    acquisition_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    cloud_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    resolution: Mapped[float] = mapped_column(Float, nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=True)
    processing_status: Mapped[ImageStatus] = mapped_column(Enum(ImageStatus), default=ImageStatus.RECEIVED)

    zone: Mapped["MonitoringZone"] = relationship("MonitoringZone", back_populates="images")
    satellite: Mapped["Satellite"] = relationship("Satellite")
    bands: Mapped[list["SpectralBand"]] = relationship("SpectralBand", back_populates="image")

class SpectralBand(Base):
    __tablename__ = "spectral_bands"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("satellite_images.id"), nullable=False)
    band_name: Mapped[str] = mapped_column(String, nullable=False) # e.g. B04
    wavelength: Mapped[float] = mapped_column(Float, nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)

    image: Mapped["SatelliteImage"] = relationship("SatelliteImage", back_populates="bands")
