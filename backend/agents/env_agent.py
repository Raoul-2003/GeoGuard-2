import asyncio
from .schemas import EnvResult

class GeoGuardEnvAgent:
    """Agent responsable du calcul des indices environnementaux (NDVI, NBR, etc)."""
    
    async def analyze(self, image_id: str, zone_id: str) -> EnvResult:
        await asyncio.sleep(0.5)
        return EnvResult(
            ndvi_before=0.75,
            ndvi_after=0.52,
            ndvi_delta=-0.23,
            conclusion="Diminution importante de la végétation."
        )
