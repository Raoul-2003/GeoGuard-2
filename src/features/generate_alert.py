import rasterio
import numpy as np
from pathlib import Path
import json
from datetime import datetime

# ============================================================
# GEOGUARD - GENERATION DE RAPPORT ET ALERTE
# ============================================================

MASK_FILE = Path(__file__).parent.parent.parent / "data/processed/difference_mask.tif"
REPORT_DIR = Path(__file__).parent.parent.parent / "data/reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

import json

# Lecture des paramètres depuis config.json
config_file = Path(__file__).parent.parent.parent / "data" / "config.json"
ALERT_THRESHOLD_PERCENT = 2.0
if config_file.exists():
    with open(config_file, "r") as f:
        try:
            config_data = json.load(f)
            ALERT_THRESHOLD_PERCENT = config_data.get("alert_threshold", 2.0)
        except Exception:
            pass

def generate_report():
    print("=" * 70)
    print("GEOGUARD - RAPPORT ET ALERTES")
    print("=" * 70)
    
    if not MASK_FILE.exists():
        print("Erreur : Masque d'anomalie introuvable. Veuillez exécuter la détection de changement.")
        return
        
    print("\n[1/2] Analyse du masque d'anomalie...")
    with rasterio.open(MASK_FILE) as src:
        mask = src.read(1)
        
    total_pixels = mask.size
    changed_pixels = np.sum(mask == 255)
    change_percent = (changed_pixels / total_pixels) * 100
    
    print(f"Surface totale analysée : {total_pixels} pixels")
    print(f"Surface impactée : {changed_pixels} pixels ({change_percent:.2f}%)")
    
    print("\n[2/2] Génération du rapport...")
    status = "CRITICAL" if change_percent > ALERT_THRESHOLD_PERCENT else "NORMAL"
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "aoi": "Abidjan (Zone Pilote)",
        "change_percent": round(change_percent, 2),
        "status": status,
        "message": f"Changement détecté sur {change_percent:.2f}% de la zone.",
        "alert_triggered": status == "CRITICAL"
    }
    
    report_file = REPORT_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)
        
    print(f"Rapport sauvegardé : {report_file}")
    
    # Simulation de l'alerte
    if status == "CRITICAL":
        print("\n" + "!" * 70)
        print("!!! ALERTE GEOGUARD DÉCLENCHÉE !!!")
        print(f"Anomalie critique détectée: {change_percent:.2f}% de modification.")
        print("Une équipe d'intervention doit être notifiée immédiatement.")
        print("!" * 70 + "\n")
    else:
        print("\n[INFO] Aucun changement critique détecté. Aucune alerte déclenchée.")
        
if __name__ == "__main__":
    generate_report()
