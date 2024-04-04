"""
copyright: 2022 EUMETSAT
license: ../LICENSE.txt

A general tools module with functions for manipulating EUMETSAT marine data.

This module contains functions for manipulating EUMETSAT marine data. It is part
of the eumartools toolkit.

  Typical usage example:

  import eumartools

  mask = eumartools.flag_mask(applied_flags, flag_names, flag_values, flags)
"""

import numpy as np
import xarray as xr


def flag_mask(flag_file, flag_variable, applied_flags, test=False, dtype=None):
    """Function to build a binary mask from specific flags.

    Args:
        flag_file (string): the netCDF format file containing the flags
        flag_variable (string): the name of the flag field in flag_file
        applied_flags (list): names of flags to apply, as list of strings
        test (bool): test case switch

    Returns:
        if succesful & test is true (int); sum of flag binary flag mask
        if succesful & test is false (numpy.ndarray); binary flag mask
        if unsuccessful (string); error message

    """
    try:
        flag_fid = xr.open_dataset(flag_file)
        flags = flag_fid.get(flag_variable).data
        flag_names = flag_fid.get(flag_variable).flag_meanings.split(" ")
        flag_values = flag_fid.get(flag_variable).flag_masks
        flag_fid.close()
    except OSError as error:
        msg = "Unsuccessful!", error, "occurred."
        print(msg)
        return msg

    try:
        if not dtype:
            flag_bits = np.zeros(np.shape(flags), np.dtype(type(flags[0][0])))
        else:
            flag_bits = np.zeros(np.shape(flags), dtype)

        for flag in applied_flags:
            try:
                flag_bits = flag_bits | flag_values[flag_names.index(flag)]
            except TypeError:
                print(flag + " not present")

        if test:
            return np.sum(np.sum((flags & flag_bits) > 0))

        return (flags & flag_bits) > 0

    except Exception as error:
        msg = "Unsuccessful!", error, "occurred."
        print(msg)
        return msg
