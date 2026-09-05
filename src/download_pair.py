import os
import datetime
from pathlib import Path
from urllib.parse import urlparse

import geopandas as gpd
import rasterio
from rasterio.mask import mask
from pystac_client import Client
import boto3

# ============================================================
# GEOGUARD - ACQUISITION DE DONNEES EN PAIRE (HISTORIQUE / RECENT)
# ============================================================

AOI_FILE = Path(__file__).parent.parent / "data/aoi/aoi_abidjan.geojson"
STAC_URL = "https://stac.dataspace.copernicus.eu/v1"
OUTPUT_DIR = Path(__file__).parent.parent / "data/raw/sentinel2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def find_best_image(catalog, geometry, start_date_str, end_date_str, max_cloud_cover=20):
    """Recherche la meilleure image (moins nuageuse) sur une période donnée."""
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        intersects=geometry,
        datetime=f"{start_date_str}/{end_date_str}",
        query={"eo:cloud_cover": {"lte": max_cloud_cover}},
        max_items=50,
    )
    items = list(search.items())
    if not items:
        return None
    # Trier par couverture nuageuse
    items.sort(key=lambda x: x.properties.get("eo:cloud_cover", 100))
    return items[0]

def download_and_crop(item, aoi_geometry, output_filename):
    """Télécharge la bande B04 d'un item STAC et la découpe selon l'AOI."""
    print(f"\nPréparation du téléchargement de {item.id}...")
    asset = item.assets.get("B04_10m")
    if not asset:
        raise RuntimeError("Bande B04_10m introuvable dans cet item.")
        
    s3_url = asset.href
    parsed = urlparse(s3_url)
    if parsed.scheme != "s3":
        raise RuntimeError(f"Type d'URL inattendu : {parsed.scheme}")
        
    bucket = parsed.netloc
    key = parsed.path.lstrip("/")
    
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    s3 = boto3.client(
        "s3",
        endpoint_url="https://eodata.dataspace.copernicus.eu",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )
    
    temp_file = OUTPUT_DIR / f"temp_{item.id}.jp2"
    out_file = OUTPUT_DIR / output_filename
    
    print(f"Téléchargement depuis S3: {bucket}/{key}")
    try:
        s3.download_file(bucket, key, str(temp_file))
    except Exception as e:
        raise RuntimeError(f"Échec du téléchargement: {e}")
        
    print("Découpage selon l'AOI...")
    with rasterio.open(temp_file) as src:
        # Convertir l'AOI dans le même système que l'image
        aoi_raster = aoi_geometry.to_crs(src.crs)
        clipped, transform = mask(src, aoi_raster.geometry, crop=True)
        profile = src.profile.copy()
        profile.update(
            driver="GTiff",
            height=clipped.shape[1],
            width=clipped.shape[2],
            transform=transform
        )
        with rasterio.open(out_file, "w", **profile) as dst:
            dst.write(clipped)
            
    # Nettoyage
    temp_file.unlink()
    print(f"Image enregistrée : {out_file}")
    return out_file

def run_download_pair():
    print("=" * 70)
    print("GEOGUARD - TELECHARGEMENT DE PAIRES D'IMAGES (HISTORIQUE & RECENT)")
    print("=" * 70)
    
    # 1. Chargement de l'AOI
    print("\n[1/4] Chargement de l'AOI...")
    aoi = gpd.read_file(AOI_FILE)
    if aoi.crs is None:
        raise ValueError("L'AOI n'a pas de système de coordonnées.")
    aoi_wgs84 = aoi.to_crs("EPSG:4326")
    geometry = aoi_wgs84.geometry.iloc[0].__geo_interface__
    
    # 2. Connexion STAC
    print("\n[2/4] Connexion au catalogue Copernicus...")
    catalog = Client.open(STAC_URL)
    
    # Dates
    today = datetime.date.today()
    one_year_ago = today - datetime.timedelta(days=365)
    
    # Plages de 90 jours pour trouver une bonne image (Abidjan est souvent nuageux)
    recent_start = (today - datetime.timedelta(days=90)).strftime("%Y-%m-%d")
    recent_end = today.strftime("%Y-%m-%d")
    
    hist_start = (one_year_ago - datetime.timedelta(days=45)).strftime("%Y-%m-%d")
    hist_end = (one_year_ago + datetime.timedelta(days=45)).strftime("%Y-%m-%d")
    
    # 3. Recherche
    print("\n[3/4] Recherche des meilleures images (Nuages < 40%)...")
    print(f" - Période récente : {recent_start} à {recent_end}")
    item_recent = find_best_image(catalog, geometry, recent_start, recent_end, max_cloud_cover=40)
    
    print(f" - Période historique: {hist_start} à {hist_end}")
    item_hist = find_best_image(catalog, geometry, hist_start, hist_end, max_cloud_cover=40)
    
    if not item_recent:
        print("Erreur: Aucune image récente trouvée sous le seuil de nuages.")
        return
    if not item_hist:
        print("Erreur: Aucune image historique trouvée sous le seuil de nuages.")
        return
        
    print(f"Image récente trouvée : {item_recent.id} ({item_recent.properties.get('eo:cloud_cover')} % nuages)")
    print(f"Image historique trouvée : {item_hist.id} ({item_hist.properties.get('eo:cloud_cover')} % nuages)")
    
    # 4. Téléchargement
    print("\n[4/4] Téléchargement et traitement...")
    try:
        download_and_crop(item_recent, aoi, "recent_b04.tif")
        download_and_crop(item_hist, aoi, "historical_b04.tif")
        print("\n[OK] Succès : Paire d'images téléchargée avec succès !")
    except Exception as e:
        print(f"\n[Erreur] Le téléchargement a échoué : {e}")

if __name__ == "__main__":
    run_download_pair()
