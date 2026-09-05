import geopandas as gpd
from pystac_client import Client
from pathlib import Path

def get_dashboard_stats():
    """
    Retourne les statistiques dynamiques pour le tableau de bord
    en réutilisant la logique des scripts GeoGuard.
    """
    stats = {
        "monitored_zones": 1,
        "risk_zones": 0,
        "active_alerts": 0,
        "analyzed_images": 0,
        "recent_alerts": []
    }
    
    # Lecture des rapports générés par l'IA
    reports_dir = Path(__file__).parent.parent / "data" / "reports"
    if reports_dir.exists():
        import json
        
        # Trouver tous les fichiers json et les trier par date (le plus récent en premier)
        report_files = sorted(reports_dir.glob("*.json"), reverse=True)
        
        for rf in report_files[:5]: # On prend les 5 plus récents
            try:
                with open(rf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                # Si c'est critique, on incrémente l'alerte
                if data.get("status") == "CRITICAL":
                    stats["active_alerts"] += 1
                    stats["risk_zones"] = 1
                    
                stats["recent_alerts"].append({
                    "title": "Anomalie Critique Détectée" if data.get("status") == "CRITICAL" else "Analyse Normale",
                    "message": data.get("message", ""),
                    "time": data.get("timestamp", "").split("T")[0] + " " + data.get("timestamp", "").split("T")[1][:5] if "T" in data.get("timestamp", "") else "",
                    "status": data.get("status")
                })
            except Exception as e:
                print(f"Erreur de lecture du rapport {rf}: {e}")
    
    # 1. Compter les zones surveillées (fichiers dans data/aoi/)
    aoi_dir = Path(__file__).parent.parent / "data" / "aoi"
    if aoi_dir.exists():
        stats["monitored_zones"] = len(list(aoi_dir.glob("*.geojson")))

    # 2. Récupérer le nombre d'images Sentinel-2 analysées/disponibles
    aoi_file = aoi_dir / "aoi_abidjan.geojson"
    if aoi_file.exists():
        try:
            aoi = gpd.read_file(aoi_file).to_crs("EPSG:4326")
            geometry = aoi.geometry.iloc[0].__geo_interface__
            
            STAC_URL = "https://stac.dataspace.copernicus.eu/v1"
            catalog = Client.open(STAC_URL)
            search = catalog.search(
                collections=["sentinel-2-l2a"],
                intersects=geometry,
                datetime="2026-05-01/2026-08-25",
                query={"eo:cloud_cover": {"lte": 20}},
                max_items=50
            )
            items = list(search.items())
            stats["analyzed_images"] = len(items)
            
            # Si on a trouvé des images avec moins de 10% de nuages, on peut considérer ça comme des "zones sans risque d'occlusion"
            stats["risk_zones"] = len([i for i in items if i.properties.get("eo:cloud_cover", 100) > 15])
            
        except Exception as e:
            print(f"Erreur lors de la récupération des stats STAC: {e}")
            
    return stats
