import geopandas as gpd
from shapely.geometry import box
from pathlib import Path

# ============================================================
# GEOGUARD - CREATION DE LA ZONE PILOTE
# ============================================================

# Centre approximatif d'Abidjan
longitude_centre = -4.00167
latitude_centre = 5.35444

# Zone d'environ 10 km x 10 km
# ~0,045 degré correspond approximativement à 5 km
demi_largeur = 0.045
demi_hauteur = 0.045

# Création du rectangle
aoi = box(
    longitude_centre - demi_largeur,
    latitude_centre - demi_hauteur,
    longitude_centre + demi_largeur,
    latitude_centre + demi_hauteur
)

# Création du GeoDataFrame
gdf = gpd.GeoDataFrame(
    {
        "nom": ["GeoGuard - Zone pilote Abidjan"],
        "ville": ["Abidjan"],
        "pays": ["Côte d'Ivoire"]
    },
    geometry=[aoi],
    crs="EPSG:4326"
)

# Création du dossier si nécessaire
output_dir = Path("data/aoi")
output_dir.mkdir(parents=True, exist_ok=True)

# Export GeoJSON
output_file = output_dir / "aoi_abidjan.geojson"
gdf.to_file(output_file, driver="GeoJSON")

print("=" * 55)
print("GEOGUARD - ZONE PILOTE")
print("=" * 55)

print(f"Fichier créé : {output_file}")
print(f"CRS : {gdf.crs}")

print("\nEmprise géographique :")
print(gdf.total_bounds)

print("\nZone créée avec succès !")
