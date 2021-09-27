#!/usr/bin/env python
# coding: utf-8

# This processes output csv files from ArcGIS into files that are injested into the pipeline.
# Specifically, read in ArcGIS csv files, extract relevant coordinates, and them write out to
#     another, 'processed' csv with additional info in a header

import ephem
import skyfield
import pandas as pd
import numpy as np
import ipdb

# read in raw file as written out by ArcGIS
df = pd.read_csv("./data/test.csv")
ipdb.set_trace()

scotland_df = df.where(np.logical_and(df["Join_Count"] == 1,df["NAME_1"] == "Scotland")).dropna(how="all")

# write out coordinates file with a header

processed_file_name = "test_processed.csv"
hdr = open(processed_file_name, "w")

hdr.write('KEY;VALUE;COMMENT;REF\n')
hdr.write('technical_string;scotland;;\n')
hdr.write('display_string;Scotland;;\n')
hdr.write('start_date;1707 May 1;Treaty of Union;Wikipedia\n')
hdr.write('end_date;-99999;;\n')
hdr.write('other;;;\n')

hdr.write('##############################\n')

scotland_df.to_csv(hdr)
print("Wrote out " + processed_file_name)
