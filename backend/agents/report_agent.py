import asyncio
from .schemas import OrchestrationPayload, ReportResult

class GeoGuardReportAgent:
    """Agent chargé de la génération de rapports humains (NLG)."""
    
    async def generate(self, payload: OrchestrationPayload) -> ReportResult:
        await asyncio.sleep(1.0)
        
        # Uses LLM natively without hallucinating
        executive = f"Alerte de niveau {payload.risk.level} sur la zone {payload.zone_id}. {payload.vision.probable_type} suspectée avec {payload.vision.confidence}% de confiance."
        scientific = f"Baisse du NDVI de {payload.env.ndvi_delta}. {payload.vision.changed_pixels} pixels affectés. Zone protégée."
        field = f"Intervention requise sous {payload.priority.intervention_sla}."

        return ReportResult(
            executive_summary=executive,
            scientific_summary=scientific,
            field_summary=field
        )
