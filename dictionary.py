import geopandas as gpd

shp_path = './data/manila/hotosm_phl_points_of_interest_points_shp.shp'
gdf = gpd.read_file(shp_path)

print("Columns in your data:", gdf.columns)

if 'amenity' in gdf.columns:
    print("\nTop Amenities found:")
    print(gdf['amenity'].value_counts().head(30))

if 'shop' in gdf.columns:
    print("\nTop Shops found:")
    print(gdf['shop'].value_counts().head(30))