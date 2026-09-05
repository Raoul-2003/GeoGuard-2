import geopandas as gpd
from pystac_client import Client
from pathlib import Path

# ============================================================
# GEOGUARD - RECHERCHE SENTINEL-2
# ============================================================

# 1. Charger notre AOI
aoi_file = Path("data/aoi/aoi_abidjan.geojson")
aoi = gpd.read_file(aoi_file)

# Vérification du système de coordonnées
if aoi.crs is None:
    raise ValueError("L'AOI n'a pas de système de coordonnées.")

aoi = aoi.to_crs("EPSG:4326")

# Géométrie GeoJSON pour STAC
geometry = aoi.geometry.iloc[0].__geo_interface__

# 2. Connexion au catalogue STAC Copernicus
STAC_URL = "https://stac.dataspace.copernicus.eu/v1"

print("=" * 65)
print("GEOGUARD - RECHERCHE SENTINEL-2")
print("=" * 65)

print("\nConnexion au catalogue Copernicus...")

catalog = Client.open(STAC_URL)

print("Connexion réussie.")

# 3. Paramètres de recherche
#
# On prend les 90 derniers jours environ.
# Pour commencer, on accepte jusqu'à 20 % de couverture nuageuse.

search = catalog.search(
    collections=["sentinel-2-l2a"],
    intersects=geometry,
    datetime="2026-05-01/2026-08-25",
    query={
        "eo:cloud_cover": {
            "lte": 20
        }
    },
    max_items=20,
)

# 4. Récupération des résultats
items = list(search.items())

print(f"\nNombre d'images trouvées : {len(items)}")

# 5. Affichage des résultats
if not items:
    print("\nAucune image trouvée avec ces critères.")
else:
    print("\nImages disponibles :")
    print("-" * 65)

    for i, item in enumerate(items, start=1):

        cloud_cover = item.properties.get("eo:cloud_cover", "N/A")

        print(f"\n{i}. {item.id}")
        print(f"   Date    : {item.datetime}")
        print(f"   Nuages  : {cloud_cover}%")

print("\n" + "=" * 65)
print("Recherche terminée.")
print("=" * 65)
