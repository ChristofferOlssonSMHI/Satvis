"""Handling of raw data to create dataframes suitable for SATvis"""
import os

import geopandas as gpd
import pandas as pd
import shapely

from satvis.writers import to_gpkg
from satvis._config import cyano_data_shp

# TODO Set globally
gpd.options.io_engine = "pyogrio"

def generate_filepaths(
    directory, pattern='', not_pattern='DUMMY_PATTERN', 
    pattern_list=None, endswith='', only_from_dir=True):
    pattern_list = [] if pattern_list is None else pattern_list
    
    for path, _subdir, fids in os.walk(directory):
        if only_from_dir:
            if path != directory:
                continue
        for f in fids:
            if pattern in f and not_pattern not in f and f.endswith(endswith):
                if any(pattern_list):
                    for pat in pattern_list:
                        if pat in f:
                            yield os.path.abspath(os.path.join(path, f))
                else:
                    yield os.path.abspath(os.path.join(path, f))

def validate_data():
    """Validates the geometries of the cyanoacteria bloom GeoDataFrames
    """
    # TODO
    # - Check for multiple years in same file
    pass

def cyano_season_gpkg():
    """Creates a gpkg file from the daily shape-files produced by BAWS.
    
    The raw file data are concatenated into a single GeoDataFrame spanning 
    a season with one row per polygon.
    """
    # TODO Add filter so it only accepts data from specific year
    data_files = generate_filepaths(directory=cyano_data_shp, endswith='.shp')

    gdfs = []
    for cyano_data_file in data_files:
        gdf = gpd.read_file(cyano_data_file)
        # I think it's better to create a date column instead of the old
        # filename since it only includes the date as an identifier
        file_ts = pd.Timestamp(
            os.path.basename(cyano_data_file)
            .split('.')[0].split('_')[-1]
            )
        gdf.insert(0, 'date', file_ts)
        gdfs.append(gdf)
    cyano_shp_gdf = pd.concat(gdfs)
    print(cyano_shp_gdf.head())
    year = cyano_shp_gdf['date'].dt.year.unique()[0]
    to_gpkg(cyano_shp_gdf, f'cyano_daymap_{year}')

def cyano_season_second_pass(gdf):
    """Cleans the raw data produced by cyano_season_gpkg."""
    # TODO 
    if not gdf['geometry'].is_valid.any():
        print('True')
    else:
        print('false')    

    # Insert date column with extracted timestamp from filename column
    gdf.insert(1, 'date', gdf['from_file'].str.extract(str(r'_(\d{8})\.')))
    gdf['date'] = pd.to_datetime(gdf['date'])

def area_and_centroid_coords(geom):
    """returns a string of polygon area and centroid coordinates"""
    # For example: 2954918.3 761397.9 7093049.7
    area = round(geom.area, 1)
    centroid = geom.centroid
    x = round(centroid.x, 1)
    y = round(centroid.y, 1)
    value = f"{area} {x} {y}"
    
    return value

def area_day_count(gdf):
    """Returns dataframe of day count with blooms per geom."""
    # Create one multiline of all polygon boundaries
    union = shapely.ops.unary_union(gdf.boundary)

    # Polygonize it and create a dataframe
    polygonized = list(shapely.ops.polygonize(union))
    gdf2 = gpd.GeoDataFrame(geometry=polygonized, crs=gdf.crs)

    # Intersect the input gdf with the polygonized gdf. 
    # Duplicate geometries till be created Where multiple polygons overlap
    area_days = gpd.overlay(
        df1=gdf, df2=gdf2, how="intersection", keep_geom_type=True
    )

    # Create a unique string to groupby
    area_days["geometry_distinction"] = area_days.apply(
        lambda x: area_and_centroid_coords(x.geometry), axis=1)

    # Creates column containing the overlap count of each polygon
    area_days["n_overlaps"] = area_days.groupby(
        "geometry_distinction", as_index=False
    )["geometry_distinction"].transform("count")
    
    return area_days


def make_basin_geopackage(basins_shp_path):
    # TODO check structure of SVAR_2016
    """Method to recreate the Baltic Sea sub-basins GeoPackage 
    
    Sub-basin geometries according to Havsomr_SVAR_2016_3b.
    """
    basin_mapping_SVAR = {
        1: 'Bottenviken',
        2: 'Norra Kvarken',
        3: 'Bottenhavet',
        4: 'Ålands hav',
        5: 'Skärgårdshavet',
        6: 'Finska viken',
        7: 'Norra Gotlandshavet',
        8: 'Västra Gotlandshavet',
        9: 'Östra Gotlandshavet',
        10: 'Rigabukten',
        11: 'Gdanskbukten',
        12: 'Bornholmshavet och Hanöbukten',
        13: 'Arkonahavet och Södra Öresund',
        14: 'Bälthavet',
        15: 'Öresund',
        16: 'Kattegatt',
        17: 'Skagerrak',
    }
    
    # TODO Rename sub_basin_shp to be easily identified
    # TODO add file as argument
    basin_gdf = gpd.read_file(basins_shp_path)
    print(basin_gdf)
    basin_geometries = basin_gdf[['BASIN_NR', 'geometry']]
    print(basin_geometries)
    basin_data = basin_geometries.dissolve(
        by='BASIN_NR', as_index=True)
    basin_data['basin_name'] = [
        basin_mapping_SVAR[item] for item in basin_data.index]
    print(basin_data)
    to_gpkg(basin_data, 'sub_basins')
    print('After to_gpkg')
    
# def make_cyano_season_geopackages(data_files):
#     """Method to recreate the cyano bloom season GeoPackage files.
    
#     Only aggregates the raw data and doesn't perform any computations.
#     Its main function is to preserve the raw data produced using the 
#     prior method.
#     """
#     # TODO Generalize
#     # Read files into a list of tables
#     # TODO Generator for self.cyano_data_shp
#     data_files = generate_filepaths(directory=cyano_data_shp)

#     for year in range(2002, 2024):
#         year = str(year) # Move str to range()?
#         geodataframes = []
#         for cyano_data_file in data_files:
#             gdf = gpd.read_file(cyano_data_file)
#             # filename = os.path.basename(cyano_data_file)
#             file_ts = pd.Timestamp(os.path.basename(cyano_data_file).split('.')[0].split('_')[-1])
#             # For each table, add new column with timestamp (or original file name if useful)
#             gdf.insert(0, 'date', file_ts)
#             geodataframes.append(gdf)
#         cyano_shp_dataframe = pd.concat(geodataframes)
#         cyano_shp_dataframe.to_file(f'cyano_daymap_{year}.gpkg')