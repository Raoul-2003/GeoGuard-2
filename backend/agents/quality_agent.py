import random
import asyncio
from .schemas import QualityResult

class GeoGuardQualityAgent:
    """Agent responsable de la validation des images satellites."""
    
    async def analyze(self, image_id: str) -> QualityResult:
        # Mock logic: in production, reads image metadata or runs lightweight CNN
        await asyncio.sleep(0.5)
        cloud_cover = random.uniform(0, 15)
        ready = cloud_cover < 10.0
        
        issues = []
        if not ready:
            issues.append(f"Couverture nuageuse trop élevée: {cloud_cover:.1f}%")

        return QualityResult(
            ready=ready,
            quality_score=100.0 - cloud_cover,
            issues=issues
        )
