#!/usr/bin/env python
# coding: utf-8

# This takes processed csv files and actually does the calculation of sunrise and sunset times for each coordinate

# Made from notebook parent 2021 June 6 by E.S.

import ephem
import skyfield
import pandas as pd
import numpy as np


# Read processed csv back in

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
    
    bluffton = api.wgs84.latlon(df_processed["LAT"][ind_num], df_processed["LON"][ind_num])

    f = almanac.risings_and_settings(eph, eph['Sun'], bluffton)
    t, y = almanac.find_discrete(t0, t1, f)

    for ti, yi in zip(t, y):
        print(ti.utc_iso(), 'Rise' if yi else 'Set')
