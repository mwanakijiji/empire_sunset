#!/usr/bin/env python
# coding: utf-8

# This plots maps

# Created 2021 June 12 by E.S.

import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
#import shapefile as shp
import geopandas as gpd

# read in raw file as written out by ArcGIS
df = pd.read_csv("./data/test_anguilla.csv")

# LAT, LON coords
anguilla_df = df.where(df["Join_Count"] == 1).dropna(how="all")

# shapefile
#data = gpd.read_file("./data/01_various_shape_files/VUT.shp", SHAPE_RESTORE_SHX=True)
data = gpd.read_file("./data/01_various_shape_files/VUT.shp")

data.plot()

plt.savefig('junk.pdf')

#data.plot("geometry", cmap="Blues")

'''
ax = plt.axes(projection=ccrs.PlateCarree())

ax.scatter(anguilla_df["LON"], anguilla_df["LAT"], color="red", transform=ccrs.PlateCarree())

ax.coastlines()
ax.set_global()

# Save the plot by calling plt.savefig() BEFORE plt.show()
#plt.savefig('coastlines.pdf')
#plt.savefig('coastlines.png')

plt.show()


# In[2]:


# which projection actually distributes points equidistantly?


# In[2]:


# Cylindrical Equal Area
df_cea = pd.read_csv("./data/Export_Output_cyl_eq_area.txt")
# Web Mercator
df_wmer = pd.read_csv("./data/Export_Output_web_mercator.txt")


# In[11]:


# Cylindrical Equal Area

ax = plt.axes(projection=ccrs.SouthPolarStereo(central_longitude=0.0, globe=None))

ax.scatter(df_cea["LONG"], df_cea["LAT"], color="red", transform=ccrs.PlateCarree(), s=0.1)

ax.coastlines()
ax.set_global()
ax.set_extent((-5000000, 5000000, -5000000, 5000000), crs=ccrs.SouthPolarStereo())

# Save the plot by calling plt.savefig() BEFORE plt.show()
#plt.savefig('coastlines.pdf')
#plt.savefig('coastlines.png')

plt.show()


# In[10]:


# Web Mercator

ax = plt.axes(projection=ccrs.SouthPolarStereo(central_longitude=0.0, globe=None))

ax.scatter(df_wmer["LONG"], df_wmer["LAT"], color="red", transform=ccrs.PlateCarree(), s=0.1)

ax.coastlines()
ax.set_global()
ax.set_extent((-5000000, 5000000, -5000000, 5000000), crs=ccrs.SouthPolarStereo())

# Save the plot by calling plt.savefig() BEFORE plt.show()
#plt.savefig('coastlines.pdf')
#plt.savefig('coastlines.png')

plt.show()


# In[5]:


# ... Cylindrical Equal Area is the winner!
'''
