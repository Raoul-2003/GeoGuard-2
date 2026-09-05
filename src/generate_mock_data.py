import numpy as np
import rasterio
from rasterio.transform import from_origin
from pathlib import Path

# ============================================================
# GEOGUARD - GENERATION DE DONNEES MOCK (SIMULATION)
# ============================================================

RAW_DIR = Path(__file__).parent.parent / "data/raw/sentinel2"
RAW_DIR.mkdir(parents=True, exist_ok=True)

HIST_FILE = RAW_DIR / "historical_b04.tif"
RECENT_FILE = RAW_DIR / "recent_b04.tif"

def generate_mocks():
    print("Génération des images de test (Mock)...")
    
    # Paramètres de base pour une image 500x500 pixels
    width, height = 500, 500
    transform = from_origin(-4.10, 5.40, 0.0002, 0.0002)
    
    # Image historique : Fond homogène (ex: forêt) avec quelques variations
    hist_data = np.random.normal(loc=1000, scale=100, size=(height, width)).astype(np.float32)
    
    # Image récente : Même fond, mais on simule une "déforestation" ou "construction" (anomalie)
    rec_data = hist_data.copy()
    
    # Création d'une anomalie au centre de l'image (zone de 100x100 pixels qui change radicalement)
    # L'intensité passe de ~1000 à ~3000 (le seuil de notre script est 1500)
    rec_data[200:300, 200:300] = np.random.normal(loc=3500, scale=200, size=(100, 100)).astype(np.float32)
    
    profile = {
        'driver': 'GTiff',
        'height': height,
        'width': width,
        'count': 1,
        'dtype': 'float32',
        'crs': 'EPSG:4326',
        'transform': transform
    }
    
    # Sauvegarde
    with rasterio.open(HIST_FILE, 'w', **profile) as dst:
        dst.write(hist_data, 1)
        
    with rasterio.open(RECENT_FILE, 'w', **profile) as dst:
        dst.write(rec_data, 1)
        
    print(f"-> {HIST_FILE.name} créé.")
    print(f"-> {RECENT_FILE.name} créé.")
    print("Données prêtes pour le test !")

if __name__ == "__main__":
    generate_mocks()
