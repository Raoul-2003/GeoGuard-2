import os
import json
import google.generativeai as genai
from .schemas import (
    VisionAnalysis, RiskScore, Explanation, TerrainMission, GeoReport
)
from .tools import tool_calculate_difference, tool_read_historical_alerts

class AgentOrchestrator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.is_mock = not self.api_key
        if not self.is_mock:
            genai.configure(api_key=self.api_key)
            # Use gemini-1.5-flash as the fast default model
            self.model_name = "gemini-1.5-flash"
        else:
            self.model_name = None

    def run_analysis(self) -> GeoReport:
        print("[Orchestrator] Démarrage de l'analyse multi-agents (Gemini)...")
        
        # Pilier 2 - Collecte et prétraitement (Mocké via tool)
        diff_stats = tool_calculate_difference()
        history = tool_read_historical_alerts()
        
        print("[Agent Vision Satellite] Analyse de l'image en cours...")
        vision_data = self._run_vision_agent(diff_stats)

        print("[Agent Risque] Calcul du score de risque...")
        risk_data = self._run_risk_agent(vision_data, history)

        print("[Agent Explicabilité] Génération de l'explication...")
        explanation_data = self._run_explicability_agent(vision_data, risk_data)
        
        print("[Agent Terrain] Création des recommandations...")
        terrain_data = self._run_terrain_agent(risk_data, explanation_data)
        
        print("[Agent Rapport] Synthèse finale...")
        report = self._run_report_agent(vision_data, risk_data, explanation_data, terrain_data)

        return report

    def _call_gemini(self, prompt: str, schema: type, system_instruction: str):
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_instruction
        )
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=schema
            )
        )
        # Parse JSON into the Pydantic schema
        return schema.model_validate_json(response.text)

    def _run_vision_agent(self, stats: dict) -> VisionAnalysis:
        if self.is_mock:
            from .schemas import VisionObservation
            return VisionAnalysis(
                overall_change_detected=True,
                observations=[
                    VisionObservation(
                        type="Déforestation",
                        confidence=0.92,
                        surface_affected_ha=12.5,
                        description="Perte massive de couverture végétale détectée."
                    )
                ]
            )
        
        prompt = f"Analyse les statistiques suivantes extraites d'images satellites et détecte les anomalies: {json.dumps(stats)}"
        return self._call_gemini(
            prompt=prompt,
            schema=VisionAnalysis,
            system_instruction="Tu es l'Agent Vision Satellite GeoGuard. Tu analyses les pixels modifiés et le NDVI."
        )

    def _run_risk_agent(self, vision: VisionAnalysis, history: list) -> RiskScore:
        if self.is_mock:
            return RiskScore(score=82, level="Critique", factors=["Perte végétale rapide", "Proximité zone protégée"])
        
        prompt = f"Observations: {vision.model_dump_json()}\nHistorique: {json.dumps(history)}"
        return self._call_gemini(
            prompt=prompt,
            schema=RiskScore,
            system_instruction="Tu es l'Agent Risque GeoGuard. Tu calcules un score de 0 à 100 basé sur les anomalies."
        )

    def _run_explicability_agent(self, vision: VisionAnalysis, risk: RiskScore) -> Explanation:
        if self.is_mock:
            return Explanation(
                decision_summary="Détection déclenchée en raison d'une baisse critique du NDVI et d'un changement spectral élevé sur plus de 10 hectares.",
                key_metrics_used=["baisse NDVI 18%", "surface affectée > 10ha"]
            )
        
        prompt = f"Vision: {vision.model_dump_json()}\nRisque: {risk.model_dump_json()}"
        return self._call_gemini(
            prompt=prompt,
            schema=Explanation,
            system_instruction="Tu es l'Agent Explicabilité GeoGuard. Explique pourquoi le système a pris cette décision de manière transparente."
        )

    def _run_terrain_agent(self, risk: RiskScore, expl: Explanation) -> TerrainMission:
        if self.is_mock:
            return TerrainMission(
                priority="Urgent",
                instructions=["Se rendre au point GPS", "Vérifier la cause de déforestation", "Prendre des photos"],
                recommended_equipment=["Drone", "Caméra thermique", "Véhicule 4x4"]
            )
        
        prompt = f"Risque: {risk.model_dump_json()}\nExplication: {expl.model_dump_json()}"
        return self._call_gemini(
            prompt=prompt,
            schema=TerrainMission,
            system_instruction="Tu es l'Agent Terrain GeoGuard. Prépare une mission d'intervention pour les équipes physiques."
        )

    def _run_report_agent(self, vision: VisionAnalysis, risk: RiskScore, expl: Explanation, terrain: TerrainMission) -> GeoReport:
        if self.is_mock:
            return GeoReport(
                title="Rapport d'Alerte Critique - Secteur Banco",
                risk_level=risk.level,
                risk_score=risk.score,
                observations=vision.observations,
                executive_summary="Risque critique nécessitant une inspection terrain sous 15 jours en raison de 12 hectares détruits.",
                explanation=expl.decision_summary,
                field_mission=terrain
            )
            
        prompt = f"Vision: {vision.model_dump_json()}\nRisque: {risk.model_dump_json()}\nTerrain: {terrain.model_dump_json()}\nExplication: {expl.model_dump_json()}"
        return self._call_gemini(
            prompt=prompt,
            schema=GeoReport,
            system_instruction="Tu es l'Agent Rapport GeoGuard. Synthétise toutes les informations en un rapport exécutif professionnel."
        )
