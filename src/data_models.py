"""
Schémas de données (Data Architecture) pour GeoGuard V2.
Prêt pour une migration vers PostgreSQL + PostGIS.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# ==========================================
# BASE TERRITORIALE (Zones et Géographie)
# ==========================================
class TerritoryZone(BaseModel):
    id: str = Field(..., description="ID unique de la zone")
    name: str = Field(..., description="Nom du territoire (ex: Forêt du Banco)")
    category: str = Field(..., description="Catégorie (Urbaine, Forestière, Agricole)")
    # En PostGIS: polygon: str = Field(..., description="WKT Polygon geometry")
    coordinates: List[List[float]] = Field(description="Liste des coordonnées [lat, lng]")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ==========================================
# BASE IMAGERIE (Sources Satellites)
# ==========================================
class SatelliteImage(BaseModel):
    id: str
    zone_id: str
    source: str = Field(..., description="Sentinel-2, Landsat, etc.")
    acquisition_date: datetime
    cloud_cover_percentage: float
    resolution_m: float
    storage_path: str = Field(..., description="Chemin vers le fichier (ex: S3, local)")

# ==========================================
# BASE ANALYTIQUE (Résultats IA)
# ==========================================
class AnalysisResult(BaseModel):
    id: str
    image_id: str
    ndvi_average: float
    spectral_change_score: float
    affected_pixels: int
    ai_confidence: float = Field(..., description="Score de confiance du modèle IA")
    detected_anomalies: List[str]

# ==========================================
# BASE OPÉRATIONNELLE (Alertes & Missions)
# ==========================================
class OperationalAlert(BaseModel):
    id: str
    analysis_id: str
    risk_level: str
    risk_score: int
    status: str = Field(default="Nouvelle", description="Nouvelle, En cours, Clôturée")
    ai_explanation: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FieldMission(BaseModel):
    id: str
    alert_id: str
    assigned_to: Optional[str]
    status: str = Field(default="Créée", description="Créée, En route, Terminée")
    priority: str
    instructions: List[str]
    field_notes: Optional[str]

# ==========================================
# BASE AUDIT (Gouvernance et Sécurité)
# ==========================================
class AuditLog(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_email: str
    action: str = Field(..., description="Action effectuée (ex: Modif Seuil, Valid Alerte)")
    details: str
    ip_address: str
