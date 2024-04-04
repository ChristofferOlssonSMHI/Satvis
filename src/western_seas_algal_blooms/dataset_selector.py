from satpy import Scene, MultiScene
from datetime import datetime
from glob import glob
import os
from pyresample.geometry import AreaDefinition


start_time = datetime(2024, 2, 28, 0, 0)
end_time = datetime(2024, 3, 6, 23, 59)

western_seas_se = AreaDefinition(area_id='western_seas_se', 
                                 description='western_seas_se', 
                                 proj_id='stere', 
                                 projection={'proj': 'stere', 'lat_0': 57.3016625, 'lon_0': 11.297785},
                                 width=1884,
                                 height=1992,
                                 area_extent=(-282586.412709, -290308.210120, 282586.412709, 307359.029789)
)

class DatasetFilter:
    def __init__(self, base_dir: str, area_definition, min_open_water: float = 0):
        # self._data = data
        self._area_definition = area_definition
        self._base_dir = base_dir
        self._open_water_flags = ['LAND', 'CLOUD', 'CLOUD_AMBIGUOUS', 'CLOUD_MARGIN', 'INVALID', 'COSMETIC', 'SATURATED', 'SUSPECT', 'HISOLZEN', 'HIGHGLINT', 'SNOW_ICE']
        self._min_open_water = min_open_water
        self._scenes = []
        # self._initialize_state()
        # self.display_result()

    # def _initialize_state(self):
    #     pass
    # #     self._blended_scenes = self.multiscene_blend()

    def _scene_creator_loop(self):
        # TODO Generalise SEN3 to accept other products (mapping by readers)
        for path in glob(f"{self._base_dir}/*SEN3"):
            scn = Scene(filenames=glob(os.path.join(path, "*")), 
                    reader="olci_l2",
                    reader_kwargs=dict(mask_items=self._open_water_flags))
            rsmp_scn = self.scene_resampler(scn)
            valid_area_quotient = self.calculate_overlap(rsmp_scn)
            print(valid_area_quotient)
            if valid_area_quotient >= self._min_open_water:
                self._scenes.append(rsmp_scn)
                print(f'Added product to MultiScene ({len(self._scenes)} total)')
        
        return self._scenes

    def scene_resampler(self, scn):
        # TODO Generalise
        scn.load(['chl_nn', 'mask'])
        rsmp_scn = scn.resample(self._area_definition)
        rsmp_scn['masked_data'] = rsmp_scn['chl_nn'].where(rsmp_scn['mask'] == 0)
        
        return rsmp_scn

    def calculate_overlap(self, rsmp_scn):
        # land_mask = open_water_flags[0]
        # land_area = land_mask_scn['mask'].values
        # Invert the values of the land_mask_scn mask array
        # land_mask_scn['mask'].values = np.logical_not(land_mask_scn['mask].values)
        # water_area = land_mask_scn['mask'].values.sum() = 1431062
        rsmp_scn['mask'].values = ~rsmp_scn['mask'].values
        valid_area = rsmp_scn['mask'].values.sum()
        # TODO Generalise water area for different area definitions
        valid_area_quotient = valid_area / 1431062
        
        return valid_area_quotient

    def multiscene_blend(self):
        scenes = self._scene_creator_loop()
        if scenes:
            mscn = MultiScene(scenes)
            mscn.load(['masked_data'])
            return mscn.blend()
            # print(blended_scene)
        else:
            raise ValueError('Found no qualifying scenes.')

    # def display_result(self):
    #     filtered_scenes = self.multiscene_blend()
    #     if filtered_scenes is not None:
    #         filtered_scenes.show('masked_data')
    #     else:
    #         print("Nothing to display. Found no qualifying scenes.")

# def main():
#     df = DatasetFilter(base_dir='./data', area_definition=western_seas_se)
#     df.display_result()

# if __name__ == "__main__":
#     main()

class MultiSceneGenerator(DatasetFilter):
    def __init__(self) -> None:
        pass

DatasetFilter(base_dir='./data', area_definition=western_seas_se)