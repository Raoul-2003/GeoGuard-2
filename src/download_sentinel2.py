import geopandas as gpd
import rasterio
from rasterio.mask import mask
from pystac_client import Client
from pathlib import Path
import boto3
from urllib.parse import urlparse

# ============================================================
# GEOGUARD - TELECHARGEMENT SENTINEL-2 B04
# ============================================================

AOI_FILE = Path(__file__).parent.parent / "data/aoi/aoi_abidjan.geojson"

PRODUCT_ID = (
    "S2C_MSIL2A_20260523T103021_N0512_R108_T30NUL_"
    "20260523T154716"
)

STAC_URL = "https://stac.dataspace.copernicus.eu/v1"

OUTPUT_DIR = Path(__file__).parent.parent / "data/raw/sentinel2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TEMP_FILE = OUTPUT_DIR / "B04_10m_full.jp2"
OUTPUT_FILE = OUTPUT_DIR / "B04_10m_abidjan.tif"

def run_download(product_id=PRODUCT_ID):
    try:
        print("=" * 70)
        print("GEOGUARD - TELECHARGEMENT SENTINEL-2")
        print("=" * 70)
        
        # ------------------------------------------------------------
        # 1. Charger l'AOI
        # ------------------------------------------------------------
        
        print("\n[1/6] Chargement de l'AOI...")
        
        aoi = gpd.read_file(AOI_FILE).to_crs("EPSG:4326")
        
        print("AOI chargée.")
        
        # ------------------------------------------------------------
        # 2. Connexion au catalogue STAC
        # ------------------------------------------------------------
        
        print("\n[2/6] Connexion à Copernicus...")
        
        catalog = Client.open(STAC_URL)
        
        search = catalog.search(
            collections=["sentinel-2-l2a"],
        ids=[product_id]
        )
        
        items = list(search.items())
        
        if not items:
            raise RuntimeError("Produit Sentinel-2 introuvable.")
        
        item = items[0]
        
        print("Produit trouvé.")
        
        # ------------------------------------------------------------
        # 3. Récupérer B04
        # ------------------------------------------------------------
        
        print("\n[3/6] Recherche de B04_10m...")
        
        asset = item.assets["B04_10m"]
        
        s3_url = asset.href
        
        print("Ressource :")
        print(s3_url)
        
        # ------------------------------------------------------------
        # 4. Télécharger depuis S3
        # ------------------------------------------------------------
        
        print("\n[4/6] Téléchargement de B04_10m...")
        print("Cela peut prendre quelques instants.")
        
        parsed = urlparse(s3_url)
        
        if parsed.scheme != "s3":
            raise RuntimeError(
                f"Type d'URL inattendu : {parsed.scheme}"
            )
        
        bucket = parsed.netloc
        key = parsed.path.lstrip("/")
        
        print(f"Bucket : {bucket}")
        print(f"Objet  : {key}")
        
        import os
        
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        
        s3 = boto3.client(
            "s3",
            endpoint_url="https://eodata.dataspace.copernicus.eu",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )
        
        try:
            s3.download_file(
                bucket,
                key,
                str(TEMP_FILE)
            )
        except Exception as e:
            raise RuntimeError(
                "\nImpossible de télécharger la donnée depuis "
                "le stockage Copernicus.\n"
                f"Détail : {e}"
            )
        
        print("Téléchargement terminé.")
        
        # ------------------------------------------------------------
        # 5. Découpage selon l'AOI
        # ------------------------------------------------------------
        
        print("\n[5/6] Découpage selon l'AOI GeoGuard...")
        
        with rasterio.open(TEMP_FILE) as src:
        
            aoi_raster = aoi.to_crs(src.crs)
        
            clipped, transform = mask(
                src,
                aoi_raster.geometry,
                crop=True
            )
        
            profile = src.profile.copy()
        
            profile.update(
                driver="GTiff",
                height=clipped.shape[1],
                width=clipped.shape[2],
                transform=transform
            )
        
            with rasterio.open(
                OUTPUT_FILE,
                "w",
                **profile
            ) as dst:
                dst.write(clipped)
        
        # ------------------------------------------------------------
        # 6. Nettoyage et vérification
        # ------------------------------------------------------------
        
        TEMP_FILE.unlink()
        
        print("\n[6/6] Vérification du résultat...")
        
        with rasterio.open(OUTPUT_FILE) as src:
        
            print("\n" + "=" * 70)
            print("TELECHARGEMENT TERMINE")
            print("=" * 70)
        
            print(f"\nFichier : {OUTPUT_FILE}")
            print("CRS :", src.crs)
            print("Largeur :", src.width)
            print("Hauteur :", src.height)
            print("Résolution :", src.res)
            print("Bandes :", src.count)
            print("Type :", src.dtypes[0])
        
        print("\n[OK] Première donnée satellite GeoGuard disponible.")
        
    except Exception as e:
        print(f"Erreur lors du téléchargement: {e}")
        return False
    return True

if __name__ == "__main__":
    run_download()