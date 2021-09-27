#!/usr/bin/env python
# coding: utf-8

# This takes processed csv files and actually does the calculation of sunrise and sunset times for each coordinate

# Made from notebook parent 2021 June 6 by E.S.

import ephem
import skyfield
import pandas as pd
import numpy as np
import xarray as xr

# Read processed csv back in
processed_file_name = "test_processed_anguilla.csv"
df_processed = pd.read_csv(processed_file_name,skiprows=6)
print("Reading in " + processed_file_name)


# Ref: https://rhodesmill.org/skyfield/almanac.html

from skyfield import api
from skyfield.api import Loader
from skyfield import almanac

load = Loader('~/skyfield-data')
ts = api.load.timescale()

# load JPL ephemeri
# de440.bsp: 31-DEC-1549 00:00 to   25-JAN-2650 00:00
# de441.bsp goes to 17191 AD
eph = api.load('de440.bsp') # change so that it doesn't have to be downloaded each time

# extract start and end dates
t0 = ts.utc(1707, 5, 1, 4)
t1 = ts.utc(1707, 6, 2, 4)

# for each coordinate, calculate sunrise and sunset times for the relevant range of dates
for ind_num in range(0,len(df_processed)):

    #print(df_processed["LAT"][ind_num])
    #print(df_processed["LON"][ind_num])

    bluffton = api.wgs84.latlon(df_processed["LAT"][ind_num], df_processed["LON"][ind_num])

    f = almanac.risings_and_settings(eph, eph['Sun'], bluffton)
    t, y = almanac.find_discrete(t0, t1, f)

    for ti, yi in zip(t, y):
        print(ti.utc_iso(), 'Rise' if yi else 'Set')
import ipdb; ipdb.set_trace()

# print the UT day only (i.e., '1707-05-10T22:33:54Z' -> '1707-05-10')
# t.utc_strftime(format="%Y-%m-%d")
# insert safety catch that first two elements are the same (i.e., 1 rise and 1 set)

# generate an axis of strings denoting UT date and event (1: rise, 0: set)
# ex.: 1707-05-01_1 means 'UT 1707-05-01, rise'
epoch_axis = ([str(a) + "_" +str(b) for a,b in zip(days_array,y)])
lat_axis = df_processed["LAT"].values
lon_axis = df_processed["LON"].values

# construct a 3d xarray with axes epoch, LAT, LON
# later: add in attrs as meta-data
data = xr.DataArray(data=np.zeros((len(epoch_axis),len(lat_axis),len(lon_axis))),
                    dims=("time", "LAT", "LON"),
                    coords={"time": epoch_axis, "LAT": np.arange(len(df_processed["LAT"])), "LON":np.arange(len(df_processed["LON"]))})

chron_len = len(data["time"])
lat_len = len(data["LAT"])
lon_len = len(data["LON"])
lat_test_val = 46
lon_test_val = 33
# loop over each chronological slice
## ## THIS INELEGANT FOR-LOOP WORKS AS-IS
for t_i in range(0,chron_len):
    time_string = data["time"][t_i]
    # loop over latitude
    for lat_i in range(0,lat_len):
        lat_string = data["LAT"][lat_i]
        # loop over longitude
        for lon_i in range(0,lon_len):
            lon_string = data["LON"][lon_i]
            # insert test value 314
            cond_mask = data.where((data["time"] == time_string) & (data["LAT"] == lat_test_val) & (data["LON"] == lon_test_val))
            data[cond_mask] = 314


# print the data to file
# columns:
# [0]: UT date
# [1]: Event ('rise' or 'set')
# [2]: UT time
