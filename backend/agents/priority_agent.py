import asyncio
from .schemas import RiskResult, GeoResult, PriorityResult

class GeoGuardPriorityAgent:
    """Agent de priorisation des interventions."""
    
    async def evaluate(self, risk: RiskResult, geo: GeoResult) -> PriorityResult:
        await asyncio.sleep(0.2)
        
        priority_level = 1 if risk.level == "CRITIQUE" else (2 if risk.level == "ELEVE" else 4)
        sla = "24 heures" if priority_level == 1 else "7 jours"
        
        return PriorityResult(
            priority_level=priority_level,
            intervention_sla=sla
        )
