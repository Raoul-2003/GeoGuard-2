import numpy as np
import rasterio
from pathlib import Path

# ============================================================
# GEOGUARD - MODELE DE DETECTION DE CHANGEMENT (V1)
# ============================================================

RAW_DIR = Path(__file__).parent.parent.parent / "data/raw/sentinel2"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "data/processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HIST_FILE = RAW_DIR / "historical_b04.tif"
RECENT_FILE = RAW_DIR / "recent_b04.tif"
DIFF_FILE = OUTPUT_DIR / "difference_mask.tif"

import json

# Lecture des paramètres depuis config.json
config_file = Path(__file__).parent.parent.parent / "data" / "config.json"
THRESHOLD = 1500
if config_file.exists():
    with open(config_file, "r") as f:
        try:
            config_data = json.load(f)
            THRESHOLD = config_data.get("diff_threshold", 1500)
        except Exception:
            pass

def run_change_detection():
    print("=" * 70)
    print("GEOGUARD - DETECTION DE CHANGEMENT")
    print("=" * 70)
    
    if not HIST_FILE.exists() or not RECENT_FILE.exists():
        print("Erreur : Les images source sont introuvables. Lancez le téléchargement d'abord.")
        return

    print("\n[1/3] Chargement des images...")
    with rasterio.open(HIST_FILE) as src_hist:
        hist_data = src_hist.read(1).astype(np.float32)
        profile = src_hist.profile
        
    with rasterio.open(RECENT_FILE) as src_rec:
        rec_data = src_rec.read(1).astype(np.float32)
        
    if hist_data.shape != rec_data.shape:
        print("Erreur : Les deux images n'ont pas la même dimension.")
        return
        
    print("\n[2/3] Calcul des différences absolues...")
    # Calcul de la différence
    diff = np.abs(rec_data - hist_data)
    
    # Création du masque d'anomalie
    anomaly_mask = (diff > THRESHOLD).astype(np.uint8) * 255
    
    # Calcul des statistiques
    total_pixels = anomaly_mask.size
    changed_pixels = np.sum(anomaly_mask == 255)
    change_ratio = (changed_pixels / total_pixels) * 100
    
    print(f"-> Pixels modifiés  : {changed_pixels}")
    print(f"-> Pourcentage d'AOI touché : {change_ratio:.2f}%")
    
    print("\n[3/3] Sauvegarde du masque d'anomalie et de la visualisation...")
    profile.update(dtype=rasterio.uint8, count=1)
    with rasterio.open(DIFF_FILE, 'w', **profile) as dst:
        dst.write(anomaly_mask, 1)
        
    # Création d'une image RGB pour la visualisation avec PIL
    try:
        from PIL import Image
        
        # Normaliser l'image historique (fond) pour qu'elle soit visible (0-255)
        hist_min = hist_data.min()
        hist_max = hist_data.max() if hist_data.max() > hist_min else hist_min + 1
        hist_norm = ((hist_data - hist_min) / (hist_max - hist_min) * 255).astype(np.uint8)
        
        rec_min = rec_data.min()
        rec_max = rec_data.max() if rec_data.max() > rec_min else rec_min + 1
        rec_norm = ((rec_data - rec_min) / (rec_max - rec_min) * 255).astype(np.uint8)
        
        # Sauvegarder les images de base en niveaux de gris
        hist_vis_file = OUTPUT_DIR / "historical_vis.png"
        rec_vis_file = OUTPUT_DIR / "recent_vis.png"
        Image.fromarray(hist_norm).save(hist_vis_file)
        Image.fromarray(rec_norm).save(rec_vis_file)
        
        # Créer les canaux RGB (Image en niveaux de gris pour commencer)
        r_channel = hist_norm.copy()
        g_channel = hist_norm.copy()
        b_channel = hist_norm.copy()
        
        # Superposer l'anomalie en rouge vif (Canal R à 255, G et B à 0 là où il y a une anomalie)
        r_channel[anomaly_mask == 255] = 255
        g_channel[anomaly_mask == 255] = 0
        b_channel[anomaly_mask == 255] = 0
        
        rgb_image = np.stack([r_channel, g_channel, b_channel], axis=-1)
        
        # Sauvegarder
        vis_file = OUTPUT_DIR / "anomaly_map.png"
        Image.fromarray(rgb_image).save(vis_file)
        print(f"Visualisations sauvegardées : {vis_file.name}, {hist_vis_file.name}, {rec_vis_file.name}")
    except Exception as e:
        print(f"Erreur lors de la génération de la visualisation : {e}")
        
    print(f"Fichier TIF sauvegardé : {DIFF_FILE}")
    print("\n[OK] Détection terminée.")
    
if __name__ == "__main__":
    run_change_detection()
