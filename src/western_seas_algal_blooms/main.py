from datetime import datetime
from pyresample.geometry import AreaDefinition
from satpy import Scene, find_files_and_readers
from satpy.composites import SingleBandCompositor
from satpy.writers import to_image, get_enhanced_image
from satpy.readers.generic_image import GenericImageFileHandler
from trollimage.colormap import ylgnbu
from pycoast import ContourWriterAGG

# from PIL import Image
from trollimage.image import Image
import xarray

# western_seas_se = get_area_def('western_seas_se')
western_seas_se = AreaDefinition(
    area_id="western_seas_se",
    description="western_seas_se",
    proj_id="stere",
    projection={"proj": "stere", "lat_0": 57.3016625, "lon_0": 11.297785},
    width=1884,
    height=1992,
    area_extent=(-282586.412709, -290308.210120, 282586.412709, 307359.029789),
)

# western_seas_se:
#   description:
#     The seas bordering Sweden's west coast
#   projection:
#     proj: stere
#     ellps: WGS84
#     lat_0: 57.3016625
#     lon_0: 11.297785000000001
#   shape:
#     height: 1992
#     width: 1884
#   area_extent:
#     lower_left_xy: [-282586.412709, -290308.210120]
#     upper_right_xy: [282586.412709, 307359.029789]


def render_chl_nn():
    files = find_files_and_readers(
        sensor="olci",
        start_time=datetime(2024, 1, 1, 0, 0),
        end_time=datetime(2024, 12, 31, 23, 59),
        base_dir="",
        reader="olci_l2",
    )

    scn = Scene(filenames=files)
    print("Available datasets:", scn.available_dataset_names())
    print("Avaliable composites:", scn.available_composite_names())

    # # Custom color map
    # arr = np.array([ 0, 1, 1.8, 2.5, 4, 4.5, 5],
    #         [
    #             [0, 0, 0.5],
    #             [0, 0.3, 0.8],
    #             [1, 0.2, 0.2],
    #             [1, 0.9, 0],
    #             [0, 0.8, 0.1],
    #             [0, 0.6,0.2],
    #             [1, 1, 1],
    #       ])

    # np.save("binary_colormap.npy", arr)

    # kwargs = {"palettes": [{"filename": "binary_colormap.npy",

    #           "min_value": 0, "max_value": 303.15}]}

    # kwargs = {"palettes": [{"filename": "binary_colormap.npy"}]}

    # Constructing scene

    scn.load(["chl_oc4me"])

    compositor = SingleBandCompositor("test")

    composite = compositor((scn["chl_oc4me"],))

    # greys.set_range(0, 5)
    ylgnbu.set_range(0.6, 0.9)
    # algae_cm = ylgnbu + greys

    img = to_image(composite)
    img.colorize(ylgnbu.reverse())  # Built-in color maps
    # colorize(img, **kwargs) # Custom color map
    img.show()

    # # Coastlines
    # newscn = scn.resample('euron1')
    # newscn.show(composite, {'coast_dir': 'C:\Arbetsmapp\Shapefiler\gshhg-shp-2.3.7', 'color': (255, 255, 0), 'resolution': 'i'})

    # scn.load([composite])
    # scn.show(composite)


def render_true_color():
    files = find_files_and_readers(
        sensor="olci",
        start_time=datetime(2024, 1, 1, 0, 0),
        end_time=datetime(2024, 12, 31, 23, 59),
        base_dir=".",
        reader="olci_l2",
    )

    scn = Scene(filenames=files)
    # print('Available datasets:', scn.available_dataset_names())
    # print('Avaliable composites:', scn.available_composite_names())

    composite = "chl_nn"

    scn.load([composite])

    newscn = scn.resample(western_seas_se)

    compositor = SingleBandCompositor("test")
    composite = compositor((newscn["chl_nn"],))

    # greys.set_range(0, 5)
    ylgnbu.set_range(0.1, 1)
    # algae_cm = ylgnbu + greys

    img = get_enhanced_image(composite)
    # colorize(img, **kwargs) # Custom color map
    # enh_img = get_enhanced_image(composite, overlay={'coast_dir': 'C:\Arbetsmapp\Shapefiler\gshhg-shp-2.3.7',
    #                                         #    'color': (255, 255, 0),
    #                                         #    'resolution': 'l'})
    img.colorize(ylgnbu.reverse())  # Built-in color maps

    # proj4_string = '+proj=stere +lat_0=57.3016625 +lon_0=11.297785 +ellps=WGS84'
    # area_extent = (-282586.412709, -290308.210120, 282586.412709, 307359.029789)
    # size =
    # area_def = (proj4_string, area_extent)
    # cw = ContourWriterAGG('C:\Arbetsmapp\Shapefiler\gshhg-shp-2.3.7')
    # cw.add_coastlines(img, area_def, resolution='l', level=4)
    img.show()

    # Coastlines
    # newscn.show(composite, {'coast_dir': 'C:\Arbetsmapp\Shapefiler\gshhg-shp-2.3.7', 'color': (255, 255, 0), 'resolution': 'i'})

    # scn.load([composite])
    # scn.show(composite, {'coast_dir': 'C:\Arbetsmapp\Shapefiler\gshhg-shp-2.3.7', 'color': (255, 255, 0), 'resolution': 'i'})

    # newscn.save_datasets(writer="simple_image")


def colorize_image():
    data = GenericImageFileHandler(
        filename="chl_nn_20240304_091614",
        filename_info="chl_nn_20240304_091614.png",
        filetype_info=".png",
    )
    img = Image(data, mode="L")
    img.colorize(ylgnbu.reverse())  # Built-in color maps

    img.show()


def add_coastlines():
    # proj4_string = '+proj=stere +lat_0=57.3016625 +lon_0=11.297785 +ellps=WGS84'
    # area_extent = (-282586.412709, -290308.210120, 282586.412709, 307359.029789)
    # area_def = (proj4_string, area_extent)
    cw = ContourWriterAGG("C:\Arbetsmapp\Shapefiler\gshhg-shp-2.3.7")
    cw.add_coastlines_to_file(
        "chl_nn_20240304_091614.png", western_seas_se, resolution="f", level=1
    )


def mask_test():
    files = find_files_and_readers(
        sensor="olci",
        start_time=datetime(2024, 1, 1, 0, 0),
        end_time=datetime(2024, 12, 31, 23, 59),
        base_dir=".",
        reader="olci_l2",
    )
    scn = Scene(filenames=files)
    print("Available datasets:", scn.available_dataset_names())
    # test = DataQuery(name='mask')
    # composite = GenericCompositor('Oa01', 'Oa08', 'chl_nn')
    scn.load(["chl_nn", "mask"])
    # print(scn['mask'])
    scn["test"] = scn["chl_nn"].where(scn["mask"] == 0)
    xarray.set_options(display_max_rows=999, display_width=999)
    # scn.show('mask')
    # da = scn['mask']
    # print(da.sel(flag_meanings='LAND'))
    scn.show("test")
    # print(scn['mask'])


# render_true_color()
# colorize_image()
# add_coastlines()
mask_test()
