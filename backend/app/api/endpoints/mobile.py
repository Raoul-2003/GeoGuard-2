from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class MobileEvidence(BaseModel):
    photo_url: str
    gps_lat: float
    gps_lng: float
    timestamp: str

class MobileReportSync(BaseModel):
    mission_id: str
    agent_id: str
    ai_prediction: str
    field_validation: str  # "Confirmé", "Erreur IA", "Partiellement confirmé"
    comments: Optional[str]
    evidence: List[MobileEvidence]

@router.post("/missions/{mission_id}/sync", summary="Synchronisation Hors-Ligne Mobile")
async def sync_mobile_mission(mission_id: str, report: MobileReportSync, background_tasks: BackgroundTasks):
    """
    Endpoint appelé par l'application mobile React Native dès le retour du réseau.
    Il enregistre le rapport terrain et déclenche la Learning Loop de l'IA.
    """
    if report.mission_id != mission_id:
        raise HTTPException(status_code=400, detail="Mismatch mission ID")
        
    # Logique d'enregistrement en base (mockée ici)
    print(f"[Mobile API] Synchronisation reçue pour la mission {mission_id}")
    print(f"Validation Terrain: {report.field_validation}")
    
    # Déclenchement de la Learning Loop si l'IA s'est trompée
    if report.field_validation == "Erreur IA":
        print(f"[Learning Loop] Faux positif signalé. Envoi de la donnée {mission_id} au dataset d'entraînement.")
        
    return {"status": "success", "message": "Données synchronisées avec succès."}
