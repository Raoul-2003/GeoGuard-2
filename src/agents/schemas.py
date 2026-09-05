from pydantic import BaseModel, Field
from typing import List, Optional

class GeoLocation(BaseModel):
    lat: float = Field(..., description="Latitude of the location")
    lng: float = Field(..., description="Longitude of the location")

class VisionObservation(BaseModel):
    type: str = Field(..., description="Type of anomaly (e.g., Deforestation, Construction, Fire)")
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0")
    surface_affected_ha: float = Field(..., description="Estimated surface affected in hectares")
    description: str = Field(..., description="Details about the visual observation")

class VisionAnalysis(BaseModel):
    observations: List[VisionObservation] = Field(description="List of detected anomalies from satellite imagery")
    overall_change_detected: bool = Field(..., description="True if significant changes were detected")

class RiskScore(BaseModel):
    score: int = Field(..., description="Risk score from 0 to 100")
    level: str = Field(..., description="Risk level (Low, Medium, High, Critical)")
    factors: List[str] = Field(..., description="Key factors contributing to this risk score")

class Explanation(BaseModel):
    decision_summary: str = Field(..., description="Natural language explanation of the AI's decision")
    key_metrics_used: List[str] = Field(..., description="Metrics like 'NDVI drop of 18%'")

class TerrainMission(BaseModel):
    priority: str = Field(..., description="Mission priority (Low, Normal, Urgent)")
    instructions: List[str] = Field(..., description="Step by step instructions for field agents")
    recommended_equipment: List[str] = Field(..., description="Equipment needed for the inspection")

class GeoReport(BaseModel):
    title: str = Field(..., description="Title of the geospatial report")
    risk_level: str = Field(..., description="Overall risk level (Low, Medium, High, Critical)")
    risk_score: int = Field(..., description="Numerical risk score")
    observations: List[VisionObservation] = Field(default_factory=list)
    executive_summary: str = Field(..., description="A short summary of the findings")
    explanation: str = Field(..., description="AI explanation of the decision")
    field_mission: Optional[TerrainMission] = Field(None, description="Recommended field mission details")
