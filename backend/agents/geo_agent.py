import asyncio
from .schemas import GeoResult

class GeoGuardGeoAgent:
    """Agent spatial pour l'analyse du contexte territorial (PostGIS)."""
    
    async def analyze(self, zone_id: str) -> GeoResult:
        await asyncio.sleep(0.5)
        return GeoResult(
            human_proximity_meters=850.0,
            is_protected_area=True,
            historical_issues=True,
            conclusion="Le changement observé possède un risque élevé car situé dans une zone protégée."
        )
