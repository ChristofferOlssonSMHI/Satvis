from src.satvis._config import export_path
# from data_handler import area_day_count

# TODO Generalise gpkg writing. Make sure to do all needed calculations
# to gdf before saving

# To GeoPackage
# TODO Generalize to only save dataframe as geopackage
#     - Add arguments to create one file per time range (defaults to
#       season/year)
# def season_gpkg(bloom_gdf):
#     for year in bloom_gdf['date'].dt.year.unique():
#         bloom_gdf_season = bloom_gdf.loc[(bloom_gdf['date'] >= f'{year}-06-01') & (bloom_gdf['date'] <= f'{year}-08-31')]
#         area_days = area_day_count(bloom_gdf_season)
#         area_days.to_file(f'{year}_bloom_day_count_geometries.gpkg')

# TODO 
def to_gpkg(df, filename=None):
    filename = f'{df}.gpkg' if filename is None else filename
    df.to_file(filename, export_path)