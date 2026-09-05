import asyncio
from .schemas import OrchestrationPayload, ExplanationResult

class GeoGuardExplainabilityAgent:
    """Agent d'explicabilité de l'IA (Explainable AI - XAI)."""
    
    async def explain(self, payload: OrchestrationPayload) -> ExplanationResult:
        await asyncio.sleep(0.5)
        
        factors = [
            f"NDVI diminué de {abs(payload.env.ndvi_delta*100):.0f}%",
            f"{payload.vision.changed_pixels} pixels changés",
            "Zone protégée" if payload.geo.is_protected_area else ""
        ]
        
        return ExplanationResult(
            probable_type=payload.vision.probable_type,
            primary_factors=[f for f in factors if f],
            confidence_decomposition={
                "Image": payload.quality.quality_score,
                "Détection": payload.vision.confidence,
                "Contexte": 90.0
            }
        )
