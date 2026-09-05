import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

# Charger l'AOI
aoi_file = Path("data/aoi/aoi_abidjan.geojson")
gdf = gpd.read_file(aoi_file)

# Création de la figure
fig, ax = plt.subplots(figsize=(10, 8))

# Affichage de la zone
gdf.plot(
    ax=ax,
    facecolor="none",
    edgecolor="black",
    linewidth=2
)

# Ajouter le nom
centroid = gdf.geometry.iloc[0].centroid

ax.text(
    centroid.x,
    centroid.y,
    "ZONE PILOTE\nGEOGUARD",
    ha="center",
    va="center",
    fontsize=12
)

# Informations
ax.set_title(
    "GeoGuard - Zone pilote d'Abidjan",
    fontsize=16
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

ax.grid(True, linestyle="--", alpha=0.5)

# Sauvegarde
output_file = Path("data/aoi/aoi_abidjan.png")

plt.savefig(
    output_file,
    dpi=200,
    bbox_inches="tight"
)

plt.show()

print("=" * 55)
print("GEOGUARD - VISUALISATION AOI")
print("=" * 55)
print(f"Image créée : {output_file}")
print("Visualisation terminée avec succès !")
