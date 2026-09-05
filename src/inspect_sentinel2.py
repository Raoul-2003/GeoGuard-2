import geopandas as gpd
from pystac_client import Client
from pathlib import Path

# ============================================================
# GEOGUARD - INSPECTION D'UNE IMAGE SENTINEL-2
# ============================================================

aoi_file = Path("data/aoi/aoi_abidjan.geojson")

aoi = gpd.read_file(aoi_file).to_crs("EPSG:4326")

geometry = aoi.geometry.iloc[0].__geo_interface__

STAC_URL = "https://stac.dataspace.copernicus.eu/v1"

catalog = Client.open(STAC_URL)

product_id = (
    "S2C_MSIL2A_20260523T103021_N0512_R108_T30NUL_"
    "20260523T154716"
)

search = catalog.search(
    collections=["sentinel-2-l2a"],
    ids=[product_id]
)

items = list(search.items())

if not items:
    raise RuntimeError("Produit Sentinel-2 introuvable.")

item = items[0]

print("=" * 70)
print("GEOGUARD - INSPECTION SENTINEL-2")
print("=" * 70)

print("\nProduit :")
print(item.id)

print("\nDate :")
print(item.datetime)

print("\nCouverture nuageuse :")
print(item.properties.get("eo:cloud_cover"), "%")

print("\nBandes / ressources disponibles :")
print("-" * 70)

for name, asset in item.assets.items():
    print(f"{name:15} -> {asset.title}")

print("\nNombre de ressources :", len(item.assets))

print("\nInspection terminée.")
print("=" * 70)
