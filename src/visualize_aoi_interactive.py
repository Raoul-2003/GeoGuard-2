import geopandas as gpd
import folium
from pathlib import Path

# ============================================================
# GEOGUARD - CARTE INTERACTIVE DE L'AOI
# ============================================================

# Fichier AOI
aoi_file = Path("data/aoi/aoi_abidjan.geojson")

# Lecture du GeoJSON
gdf = gpd.read_file(aoi_file)

# Récupérer le centre de l'AOI
centroid = gdf.geometry.iloc[0].centroid

# Création de la carte
m = folium.Map(
    location=[centroid.y, centroid.x],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# Ajouter l'AOI
folium.GeoJson(
    gdf,
    name="Zone pilote GeoGuard",
    tooltip="Zone pilote GeoGuard - Abidjan",
    popup="Zone d'étude GeoGuard"
).add_to(m)

# Ajuster automatiquement la carte à l'AOI
bounds = gdf.total_bounds

m.fit_bounds([
    [bounds[1], bounds[0]],
    [bounds[3], bounds[2]]
])

# Ajouter un contrôle des couches
folium.LayerControl().add_to(m)

# Dossier de sortie
output_file = Path("data/aoi/aoi_abidjan_interactive.html")

# Sauvegarde
m.save(output_file)

print("=" * 60)
print("GEOGUARD - CARTE INTERACTIVE")
print("=" * 60)
print(f"Carte créée : {output_file}")
print("Carte interactive créée avec succès !")
