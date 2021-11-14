#!/usr/bin/env python
# coding: utf-8

# This makes plots of total amount of land (within a normalization constant)
# which is illuminated by the Sun, given LAT, LON, and sunrise and sunset times

# Created 2021 Nov. 14 by E.S.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("junk_data.csv")

# change 0s (sunsets) to -1s to enable cumulative summation that goes down when a
# sunset happens over a given (LAT,LON)
df["EVENT"].replace({0: -1}, inplace=True)

df_cumsum = df.sort_values(["JD_FULL"], ascending = (True)).reset_index(drop=True)
df_cumsum["INSOL_SUM"] = df_cumsum["EVENT"].cumsum()

plt.plot(df_cumsum["JD_FULL"],df_cumsum["INSOL_SUM"])
plt.show()
