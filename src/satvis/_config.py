from donfig import Config

# TODO Replace the commented code below. Make into dict?
config = Config('satvis', paths=['config'])

export_path = config.get('data_directories.export_path')
sentinel2_products = config.get('data_directories.sentinel2_products')
sub_basins = config.get('data_directories.sub_basins')
cyano_data_shp = config.get('data_directories.cyano_data_shp')

# with open('../../config/satvis.yaml', 'r') as f:
#     config = yaml.safe_load(f)

# dir_dict = config['data_directories']
# sub_basin_shp = dir_dict['sub_basin_shp']
# cyano_data_shp = dir_dict['cyano_data_shp']