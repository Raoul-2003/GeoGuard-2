import geopandas as gpd
from pystac_client import Client
from pathlib import Path
from shapely.geometry import shape

# ============================================================
# GEOGUARD - VERIFICATION DE COUVERTURE SENTINEL-2
# ============================================================

AOI_FILE = Path("data/aoi/aoi_abidjan.geojson")

PRODUCT_ID = (
    "S2C_MSIL2A_20260523T103021_N0512_R108_T30NUL_"
    "20260523T154716"
)

STAC_URL = "https://stac.dataspace.copernicus.eu/v1"

print("=" * 70)
print("GEOGUARD - VERIFICATION DE COUVERTURE")
print("=" * 70)

# 1. Charger l'AOI
aoi = gpd.read_file(AOI_FILE).to_crs("EPSG:4326")

aoi_geometry = aoi.geometry.iloc[0]

# 2. Connexion STAC
catalog = Client.open(STAC_URL)

# 3. Rechercher le produit
search = catalog.search(
    collections=["sentinel-2-l2a"],
    ids=[PRODUCT_ID]
)

items = list(search.items())

if not items:
    raise RuntimeError("Produit Sentinel-2 introuvable.")

item = items[0]

# 4. Récupérer l'emprise du produit
product_geometry = shape(item.geometry)

# 5. Calcul de l'intersection
intersection = aoi_geometry.intersection(product_geometry)

# 6. Vérifications
aoi_area = aoi_geometry.area
intersection_area = intersection.area

coverage = (intersection_area / aoi_area) * 100

print("\nProduit :")
print(PRODUCT_ID)

print("\nAOI GeoGuard :")
print(aoi.total_bounds)

print("\nEmprise du produit :")
print(product_geometry.bounds)

print("\nCouverture approximative de l'AOI :")
print(f"{coverage:.2f} %")

print("\nIntersection avec l'AOI :", not intersection.is_empty)

if coverage >= 99:
    print("\n[OK] La tuile couvre pratiquement toute notre AOI.")
elif coverage > 0:
    print("\n[ATTENTION] La tuile ne couvre qu'une partie de notre AOI.")
    print("Il faudra probablement compléter avec une autre tuile.")
else:
    print("\n[ERREUR] La tuile ne couvre pas notre AOI.")

print("\n" + "=" * 70)
print("Vérification terminée.")
print("=" * 70)
