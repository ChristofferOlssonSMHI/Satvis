import geopandas as gpd

from satvis.writers import to_gpkg

# TODO Fix test geometry (currently pytest throws invalid geometry object)
def test_to_gpkg(tmp_path):
    tmp_dir = tmp_path / 'test_to_gpk'
    tmp_dir.mkdir()

    geometry_data = [
        gpd.points_from_xy([1, 2], [3, 4], z=[5, 6]),
        gpd.points_from_xy([7, 8], [9, 10], z=[11, 12])
        ]
    attribute_data = ['A', 'B']

    data = list(zip(geometry_data, attribute_data))

    gdf = gpd.GeoDataFrame(data, columns=['geometry', 'attribute'])
    gdf.geometry = gdf['geometry']
    filename = 'test_gpkg'

    to_gpkg(gdf, str(tmp_dir / filename))

    assert (tmp_dir / f'{filename}.gpkg').exists()

    read_gdf = gpd.read_file(str(tmp_dir / f'{filename}.gpkg'))
    assert read_gdf.equals(gdf)