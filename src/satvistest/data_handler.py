import geopandas as gpd
import yaml

# TODO Add export dir
class DataHandler:
    def __init__(self):
        # Set GeoPandas engine as per recommendation in TODO add url
        gpd.options.io_engine = "pyogrio"

        with open('../../config/satvis.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        self.dir_dict = config['data_directories']
        self.sub_basin_shp = dir_dict['sub_basin_shp']
        cyano_data_shp = dir_dict['cyano_data_shp']

    def basin_geodataframe():
        """Method to recreate the GeoDataFrame containing the Baltic Sea
        sub-basins according to SVAR_2016.
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
        gdf_basin = gpd.read_file(self.sub_basin_shp)
        basin_geometries = gdf_basin[['BASIN_NR', 'geometry']]
        basin_data = basin_geometries.dissolve(
            by='BASIN_NR', as_index=True)
        basin_data['basin_name'] = [
            basin_mapping_SVAR[item] for item in basin_data.index]
        return basin_data

    def validate_data():
        """Validates the geometries of the cyanoacteria bloom GeoDataFrames
        """
        # TODO 
        pass

    def cyano_season_second_pass(gdf):
        """Cleans the raw data produced by cyano_season_geodataframe."""
        # TODO 
        if gdf['geometry'].is_valid.any() == False:
            print('True')
        else:
            print('false')    

        # Insert date column with extracted timestamp from filename column
        gdf.insert(1, 'date', gdf['from_file'].str.extract(str(r'_(\d{8})\.')))
        gdf['date'] = pd.to_datetime(gdf['date'])

    def cyano_season_geodataframe(data_files):
        """Method to recreate the GeoDataFrames containing the data from
        a season of cyanobacteria blooms.
        """
        # TODO Generalize
        # Read files into a list of tables
        for year in range(2002, 2024):
            year = str(year)
            geodataframes = []
            for cyano_data_file in data_files:
                gdf = gpd.read_file(cyano_data_file)
                # filename = os.path.basename(cyano_data_file)
                file_ts = pd.Timestamp(os.path.basename(cyano_data_file).split('.')[0].split('_')[-1])
                # For each table, add new column with timestamp (or original file name if useful)
                gdf.insert(0, 'date', filename)
                geodataframes.append(gdf)
            cyano_shp_dataframe = pd.concat(geodataframes)
            cyano_shp_dataframe.to_file(f'cyano_daymap_{year}.gpkg')

    def generate_filepaths(
        directory, pattern='', not_pattern='DUMMY_PATTERN', 
        pattern_list=[], endswith='', only_from_dir=True):
        for path, subdir, fids in os.walk(directory):
            if only_from_dir:
                if path != directory:
                    continue
            # Generator function (uses yield) 
            # https://docs.python.org/3/glossary.html#term-generator
            for f in fids:
                if pattern in f and not_pattern not in f and f.endswith(endswith):
                    if any(pattern_list):
                        for pat in pattern_list:
                            if pat in f:
                                yield os.path.abspath(os.path.join(path, f))
                    else:
                        yield os.path.abspath(os.path.join(path, f))