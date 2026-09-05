import geopandas as gpd
from shapely.geometry import Polygon

# Création d'une petite zone géographique fictive
zone = Polygon([
    (-4.10, 5.30),
    (-4.00, 5.30),
    (-4.00, 5.40),
    (-4.10, 5.40),
    (-4.10, 5.30)
])

# Création d'un GeoDataFrame
gdf = gpd.GeoDataFrame(
    {
        "nom": ["Zone pilote GeoGuard"],
        "risque": ["A analyser"]
    },
    geometry=[zone],
    crs="EPSG:4326"
)

print("=== GEOGUARD : TEST GEOSPATIAL ===")
print(gdf)
print("\nSystème de coordonnées :", gdf.crs)
print("\nTest réussi !")
