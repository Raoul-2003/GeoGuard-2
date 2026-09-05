import logging
from typing import Dict, Any
from .schemas import OrchestrationPayload
from .quality_agent import GeoGuardQualityAgent
from .vision_agent import GeoGuardVisionAgent
from .env_agent import GeoGuardEnvAgent
from .geo_agent import GeoGuardGeoAgent
from .risk_agent import GeoGuardRiskAgent
from .explainability_agent import GeoGuardExplainabilityAgent
from .priority_agent import GeoGuardPriorityAgent
from .report_agent import GeoGuardReportAgent
from .field_agent import GeoGuardFieldAgent

logger = logging.getLogger("GeoGuardAICoordinator")

class GeoGuardAICoordinator:
    """
    The orchestrator agent. Receives tasks, distributes them, and controls the workflow.
    """
    def __init__(self):
        self.quality_agent = GeoGuardQualityAgent()
        self.vision_agent = GeoGuardVisionAgent()
        self.env_agent = GeoGuardEnvAgent()
        self.geo_agent = GeoGuardGeoAgent()
        self.risk_agent = GeoGuardRiskAgent()
        self.explain_agent = GeoGuardExplainabilityAgent()
        self.priority_agent = GeoGuardPriorityAgent()
        self.report_agent = GeoGuardReportAgent()
        self.field_agent = GeoGuardFieldAgent()

    async def process_new_image(self, image_id: str, zone_id: str) -> OrchestrationPayload:
        logger.info(f"Coordinator: Nouvelle image reçue {image_id} pour la zone {zone_id}")
        payload = OrchestrationPayload(image_id=image_id, zone_id=zone_id)

        # 1. Quality Check
        payload.quality = await self.quality_agent.analyze(image_id)
        if not payload.quality.ready:
            logger.warning(f"Coordinator: Qualité insuffisante pour {image_id}. Fin du workflow.")
            return payload

        # 2. Parallel Analytics (Vision, Env, Geo)
        logger.info("Coordinator: Lancement des agents analytiques...")
        payload.vision = await self.vision_agent.analyze(image_id, zone_id)
        payload.env = await self.env_agent.analyze(image_id, zone_id)
        payload.geo = await self.geo_agent.analyze(zone_id)

        # 3. Decision & Risk
        logger.info("Coordinator: Calcul du risque...")
        payload.risk = await self.risk_agent.calculate(payload)
        payload.priority = await self.priority_agent.evaluate(payload.risk, payload.geo)

        # 4. Explainability
        logger.info("Coordinator: Génération de l'explication...")
        payload.explanation = await self.explain_agent.explain(payload)

        # 5. Reporting & Operations
        logger.info("Coordinator: Génération des rapports et missions...")
        payload.report = await self.report_agent.generate(payload)
        
        if payload.risk.level == "CRITIQUE":
            payload.field_mission = await self.field_agent.create_mission(payload)

        logger.info(f"Coordinator: Workflow terminé pour {image_id}")
        return payload
