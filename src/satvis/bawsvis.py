"""Takes BAWS gpkgs and transforms it for creating the end products."""
import geopandas as gpd
import pandas as pd

from satvis.data_handler import generate_filepaths
# from satvis import sub_basins, cyano_data_shp

class BawsVis:
    def __init__(
        self, bloom_data_path, sub_basins_gdf, 
        start_date=None, end_date=None, selected_basins=None
        ):
        # Date filter
        # TODO Fix pseudocode. Should determine what year files to load based on start and end year
        start_year, end_year = (start_date.dt.year, end_date.dt.year)
        year_range = [str(range(start_year, end_year + 1))] # TODO Probably needs to be str
        cyano_data_files = generate_filepaths(bloom_data_path, pattern_list=year_range)

        bloom_gdf_list = []
        for file in cyano_data_files:
            gdf = gpd.read_file(file)
            bloom_gdf_list.append(gdf)
        bloom_gdf = pd.concat(bloom_gdf_list)

        # Basin filter
        boolean_filter = sub_basins_gdf['BASIN_NR'].isin(selected_basins)
        basin_selection = sub_basins_gdf.loc[boolean_filter].set_index('BASIN_NR')

        # TODO Fix pseudocode
        bloom_gdf = bloom_gdf.where(
            bloom_gdf['date'] >= start_date &
            bloom_gdf['date'] <= end_date &
            bloom_gdf['geometry'].overlaps(basin_selection['geometry'])
            )

    def bloom_class_filter(bloom_gdf):
        """Dissolves bloom geometries and groups by date."""
        # TODO Chang to retain class separation (including clouds)
        bloom_gdf = bloom_gdf.where(bloom_gdf['class'].isin([2, 3])).dropna()
        bloom_gdf.insert(
            1, 'date', bloom_gdf['from_file'].str.extract(str(r'_(\d{8})\.'))
            )
        bloom_gdf['date'] = pd.to_datetime(bloom_gdf['date'])
        bloom_gdf = bloom_gdf[['date', 'geometry']]
        bloom_gdf = (
            bloom_gdf
            .groupby('date', as_index=False)
            .apply(lambda x: x.dissolve())
            .reset_index(drop=True)
            )
        # bloom_gdf = (
        #   bloom_gdf
        #   .groupby('date', as_index=False)
        #   .apply(lambda x: x.dissolve())
        #   .set_index('date'))

        return bloom_gdf

    def time_aggregate(self, bloom_gdf):
        """area_day_count()"""

    def basin_filter(self):
        """Cleans the data by removing geometries that don't overlap with the selected basins
        while still retaining dataframe structure
        """
        # TODO Modify to take arbitrary geom data
        # TODO Better to convert row to dataframe, perform gpd.overlay and turn back into row?
        for index, row in self.bloom_gdf.iterrows():
            day_bloom_geometry = row.geometry
            intersecting_geometry = day_bloom_geometry.intersection(self.basin_selection.unary_union)
            
            if not intersecting_geometry.is_empty:
                self.bloom_gdf.loc[index, 'geometry'] = intersecting_geometry
            else:
                # Handle the case where there is no intersection (remove the row)
                self.bloom_gdf.drop(index, inplace=True)

    def calculate_ati(self):
        """A, T and I are different normalized data about cyano blooms.
        
        A is the normalized extent of cyanobacteria blooms for the given
        time period. T is the normalized duration and I = A * T is the 
        normalized intensity.
        """
        # TODO Generalize for arbitrary date range rather than year
        year_ati = pd.DataFrame()
        for year in self.bloom_gdf['date'].dt.year.unique():
            self.bloom_gdf_year = self.bloom_gdf.loc[self.bloom_gdf['date'].dt.year == year]
            a_i = (
                self.bloom_gdf_year
                .groupby('n_overlaps')
                .apply(lambda x: x.area * x.name)
                .sum()
            )
            year_ati.loc[year, 'A'] = (a_i / len(self.bloom_gdf_year.groupby('date')))
            year_ati.loc[year, 'T'] = (a_i / self.bloom_gdf_year['geometry'].area.sum())
        year_ati['I'] = year_ati['A'] * year_ati['T']