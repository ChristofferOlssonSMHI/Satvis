# Western seas
Area extent produced by filtering the Havsomr_SVAR_2016_3b shapefile using the below argument and creating a bounding box around it
´´´"HID" IN ('580125-093104', '545500-105150', '553224-150042')´´´

To get the lon (x) and lat (y) values:
x(transform($geometry, layer_property(@layer, 'crs'),'EPSG:4326'))
y(transform($geometry, layer_property(@layer, 'crs'),'EPSG:4326'))

Get lat lon for bb corners:
min_lat: 54,746 max_lat: 59,920
min_lon: 7,314 max_lon: 15,598

Dataset selection method:
1. Retrieval
    - SentinelData
    - Geographic constraints: POLYGON ((7.256595 58.052452, 10.535889 59.956385, 10.83252 59.95501, 13.095703 56.619977, 13.183594 55.466399, 14.018555 55.541065, 14.194336 56.059769, 14.72168 56.267761, 15.79834 56.24335, 15.732422 54.059388, 14.633789 53.527248, 9.272461 53.813626, 7.256595 58.052452))
2. Selection
    - 25 % overlap function of havsomr
    - x % cloud free area 

# TODO
- WaterAreaCalculator