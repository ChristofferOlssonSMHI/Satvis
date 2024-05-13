from donfig import Config

config = Config('satvis', paths=['config'])

export_path = config.get('data_directories.export_path')
sentinel2_products = config.get('data_directories.sentinel2_products')
sub_basins = config.get('data_directories.sub_basins')
cyano_data_shp = config.get('data_directories.cyano_data_shp')