import asyncio
from .schemas import OrchestrationPayload, FieldMissionResult

class GeoGuardFieldAgent:
    """Agent opérationnel traduisant une alerte en mission terrain."""
    
    async def create_mission(self, payload: OrchestrationPayload) -> FieldMissionResult:
        await asyncio.sleep(0.5)
        
        return FieldMissionResult(
            mission_created=True,
            mission_type="Inspection de Déforestation",
            priority=f"P{payload.priority.priority_level}",
            required_equipment=["GPS", "Drone", "Appareil photo"]
        )
