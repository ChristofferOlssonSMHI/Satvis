# from satvis.writers import to_gpkg
from satvis.data_handler import make_basin_geopackage, cyano_season_gpkg

def test_make_basin_geopackage():
    make_basin_geopackage(
        '/home/janky/Data/Shapefiler/Sub-basins_Baltic_Sea/Havsomr_SVAR_2016_3b.shp'
        )

def test_cyano_season_gpkg():
    cyano_season_gpkg()

test_cyano_season_gpkg()