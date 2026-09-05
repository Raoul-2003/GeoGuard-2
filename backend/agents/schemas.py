from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QualityResult(BaseModel):
    ready: bool = Field(description="True if the image is usable for AI analysis")
    quality_score: float = Field(description="0-100 score indicating overall image quality")
    issues: List[str] = Field(default_factory=list, description="List of quality issues (e.g. 'high cloud cover')")

class VisionResult(BaseModel):
    zone_id: str
    changed_pixels: int = Field(description="Number of pixels modified")
    total_pixels: int = Field(description="Total pixels in the area of interest")
    probable_type: str = Field(description="Classification of the change (e.g. Déforestation, Urbanisation)")
    confidence: float = Field(description="0-100 confidence score from the vision model")

class EnvResult(BaseModel):
    ndvi_before: float
    ndvi_after: float
    ndvi_delta: float
    conclusion: str = Field(description="Scientific conclusion of the environmental change")

class GeoResult(BaseModel):
    human_proximity_meters: float
    is_protected_area: bool
    historical_issues: bool
    conclusion: str = Field(description="Geospatial conclusion regarding the context")

class RiskResult(BaseModel):
    risk_score: float = Field(description="GeoGuard Risk Score from 0 to 100")
    level: str = Field(description="CRITIQUE, ELEVE, MOYEN, or FAIBLE")
    recommended_action: str

class ExplanationResult(BaseModel):
    probable_type: str
    primary_factors: List[str] = Field(description="Bullet points explaining the AI's decision")
    confidence_decomposition: Dict[str, float] = Field(description="Breakdown of confidence (Image, Detection, Context)")

class PriorityResult(BaseModel):
    priority_level: int = Field(description="1 to 5, where 1 is highest priority")
    intervention_sla: str = Field(description="Recommended SLA for intervention (e.g. '24 heures')")

class ReportResult(BaseModel):
    executive_summary: str
    scientific_summary: str
    field_summary: str

class FieldMissionResult(BaseModel):
    mission_created: bool
    mission_type: str
    priority: str
    required_equipment: List[str]

class OrchestrationPayload(BaseModel):
    image_id: str
    zone_id: str
    quality: Optional[QualityResult] = None
    vision: Optional[VisionResult] = None
    env: Optional[EnvResult] = None
    geo: Optional[GeoResult] = None
    risk: Optional[RiskResult] = None
    explanation: Optional[ExplanationResult] = None
    priority: Optional[PriorityResult] = None
    report: Optional[ReportResult] = None
    field_mission: Optional[FieldMissionResult] = None
