#!/usr/bin/env python
# coding: utf-8

# This takes processed csv files and actually does the calculation of sunrise and sunset times for each coordinate

# Made from notebook parent 2021 June 6 by E.S.

import ephem
import skyfield
import pandas as pd
import numpy as np
import xarray as xr
from skyfield import api
from skyfield.api import Loader
from skyfield import almanac

# Read processed csv back in
processed_file_name = "test_processed_anguilla.csv"
df_processed = pd.read_csv(processed_file_name,skiprows=6)
print("Reading in " + processed_file_name)

# fix a strange conda/pandas conflict; see https://github.com/pandas-profiling/pandas-profiling/issues/662
pd.set_option("display.max_columns", None)


# Ref: https://rhodesmill.org/skyfield/almanac.html

load = Loader('~/skyfield-data')
ts = api.load.timescale()

# load JPL ephemeri
# de440.bsp: 31-DEC-1549 00:00 to   25-JAN-2650 00:00
# de441.bsp goes to 17191 AD
eph = api.load('de440.bsp')

# set start and end dates
t0 = ts.utc(1707, 5, 1, 4)
t1 = ts.utc(1707, 5, 10, 4)

## ## TDB dates for now; IS THAT WHAT I WANT? NOTE THAT TDB USED AGAIN LATER
## ## WHEN POPULATING THE DATAFRAME

jd_range = np.arange(np.floor(t0.tdb),np.floor(t1.tdb), dtype=int) # range of TDB Julian dates



# make new DataFrame where each stored element is the fraction to add to the JD column
# to denote the time of that event (rise or set)

# columns:
# [0]: LAT
# [1]: LON
# [2]: JD
# [3]: Event ('1=rise' or '0=set')

lat_axis = df_processed["LAT"].values
lon_axis = df_processed["LON"].values

latlon_base = df_processed[["LAT","LON"]].copy()
#data["JD"] = jd_range_repeat


# tile JD values (for sunrise and sunset); there should be a pair of identical (LAT, LON)
# for each JD value
jd_range_repeat = np.repeat(jd_range, 2*len(lat_axis))

# events: 1=rise (I THINK), 0=set
event_boolean_base = np.concatenate((np.ones(len(lat_axis)),np.zeros(len(lat_axis))))
event_boolean = np.tile(event_boolean_base, len(jd_range)).astype(int)

# make a DataFrame starting with a tiling of the LAT, LON values
data = pd.DataFrame(np.tile(latlon_base,(2*len(jd_range),1)), columns=["LAT","LON"])

# insert JDs and placeholders for fractions
data["JD_FLOOR"] = jd_range_repeat
data["JD_MOD"] = np.nan # for JD modulus
data["EVENT"] = event_boolean


# for each coordinate, calculate sunrise and sunset times for the relevant range of dates
for ind_num in range(0,len(data)):

    print(ind_num)

    bluffton = api.wgs84.latlon(data["LAT"][ind_num], data["LON"][ind_num])

    f = almanac.risings_and_settings(eph, eph['Sun'], bluffton)
    epochs_full, riseorset = almanac.find_discrete(t0, t1, f)

    # loop over each event and populate the JD_MOD column with the decimal
    # part of the JD
    for t in range(0,len(epochs_full)):

        #print(riseorset[t])
        #import ipdb; ipdb.set_trace()

        #epoch_this = epochs_full[t]
        #riseorset_this = riseorset[t]

        data.loc[((data["JD_FLOOR"] == np.floor(epochs_full.tdb[t].astype(float))) &
                (data["LAT"] == data["LAT"][ind_num]) &
                (data["LON"] == data["LON"][ind_num]) &
                (data["EVENT"] == int(riseorset[t]))), "JD_MOD"] = epochs_full.tdb[t]%1
        #cond_mask = data.where((data["JD_FLOOR"] == np.floor(epochs_full.tdb[t].astype(float))) & (data["LAT"] == data["LAT"][ind_num]) & (data["LON"] == data["LON"][ind_num]) & (data["EVENT"] == riseorset[t]))
        #import ipdb; ipdb.set_trace()
        #data["JD_MOD"][cond_mask] = epochs_full.tdb[t]%1 # get fractional day

# make new column that sums the JD whole numbers and fractions
data["JD_FULL"] = data["JD_FLOOR"] + data["JD_MOD"]



import ipdb; ipdb.set_trace()
