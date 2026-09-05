import asyncio
from .schemas import OrchestrationPayload, RiskResult

class GeoGuardRiskAgent:
    """Agent d'évaluation du risque global (GeoGuard Risk Score)."""
    
    async def calculate(self, payload: OrchestrationPayload) -> RiskResult:
        await asyncio.sleep(0.5)
        
        # Formule indicative (mock)
        # 30% changement, 25% sensibilité, 20% historique, 15% humain, 10% env
        
        score = 87.0
        level = "CRITIQUE" if score > 80 else ("ELEVE" if score > 60 else "MOYEN")

        return RiskResult(
            risk_score=score,
            level=level,
            recommended_action="Mission terrain recommandée." if level == "CRITIQUE" else "Surveillance accrue."
        )
