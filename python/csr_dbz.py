from datetime import datetime 
print(datetime.now())

import numpy as np
from matplotlib import pyplot
from matplotlib.cm import get_cmap
from matplotlib.colors import from_levels_and_colors
from cartopy import crs
from cartopy.feature import NaturalEarthFeature, COLORS
from netCDF4 import Dataset
from wrf import (getvar, to_np, get_cartopy, latlon_coords, vertcross,
                 cartopy_xlim, cartopy_ylim, interpline, CoordPair)

# Open the NetCDF file
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/WDM6/"
wrf_file = Dataset(path+"wrfout_d03_2017-07-04_12:00:00")

# Define the cross section start and end points
cross_start  = CoordPair(lat=33.36, lon=129.5)
cross_end = CoordPair(lat=33.36, lon=133.5)

# Get the WRF variables
ht = getvar(wrf_file, "z", timeidx=132)
ter = getvar(wrf_file, "ter", timeidx=132)
dbz = getvar(wrf_file, "dbz", timeidx=132)
max_dbz = getvar(wrf_file, "mdbz", timeidx=132)
Z = 10**(dbz/10.) # Use linear Z for interpolation

wspd =  getvar(wrf_file, "uvmet_wspd_wdir", units="kt",timeidx=132)
wa=getvar(wrf_file, "wa", units="kt",timeidx=132)

# Compute the vertical cross-section interpolation.  Also, include the
# lat/lon points along the cross-section in the metadata by setting latlon
# to True.
z_cross = vertcross(Z, ht, wrfin=wrf_file,
                    start_point=cross_start,
                    end_point=cross_end,
                    latlon=True, meta=True)

# Convert back to dBz after interpolation
dbz_cross = 10.0 * np.log10(z_cross)



# Add back the attributes that xarray dropped from the operations above
dbz_cross.attrs.update(z_cross.attrs)
dbz_cross.attrs["description"] = "radar reflectivity cross section"
dbz_cross.attrs["units"] = "dBZ"

wspd_cross = vertcross(wspd, ht, wrfin=wrf_file, start_point=cross_start,
                       end_point=cross_end, latlon=True, meta=True)
wspd_cross.attrs.update(z_cross.attrs)

wa_cross = vertcross(wa, ht, wrfin=wrf_file, start_point=cross_start,
                       end_point=cross_end, latlon=True, meta=True)
wa_cross.attrs.update(z_cross.attrs)


# To remove the slight gap between the dbz contours and terrain due to the
# contouring of gridded data, a new vertical grid spacing, and model grid
# staggering, fill in the lower grid cells with the first non-missing value
# for each column.

# Make a copy of the z cross data. Let's use regular numpy arrays for this.
dbz_cross_filled = np.ma.copy(to_np(dbz_cross))

# For each cross section column, find the first index with non-missing
# values and copy these to the missing elements below.
for i in range(dbz_cross_filled.shape[-1]):
    column_vals = dbz_cross_filled[:,i]
    # Let's find the lowest index that isn't filled. The nonzero function
    # finds all unmasked values greater than 0. Since 0 is a valid value
    # for dBZ, let's change that threshold to be -200 dBZ instead.
    first_idx = int(np.transpose((column_vals > -200).nonzero())[0])
    dbz_cross_filled[0:first_idx, i] = dbz_cross_filled[first_idx, i]

# Get the terrain heights along the cross section line
ter_line = interpline(ter, wrfin=wrf_file, start_point=cross_start,
                      end_point=cross_end)

# Get the lat/lon points
lats, lons = latlon_coords(dbz)

# Get the cartopy projection object
cart_proj = get_cartopy(dbz)

# Create the figure
fig = pyplot.figure(figsize=(8,6))
ax_cross = pyplot.axes()

dbz_levels = np.arange(5., 75., 5.)

# Create the color table found on NWS pages.
dbz_rgb = np.array([[4,233,231],
                    [1,159,244], [3,0,244],
                    [2,253,2], [1,197,1],
                    [0,142,0], [253,248,2],
                    [229,188,0], [253,149,0],
                    [253,0,0], [212,0,0],
                    [188,0,0],[248,0,253],
                    [152,84,198]], np.float32) / 255.0

dbz_map, dbz_norm = from_levels_and_colors(dbz_levels, dbz_rgb,
                                           extend="max")

# Make the cross section plot for dbz
dbz_levels = np.arange(5.,75.,5.)
xs = np.arange(0, dbz_cross.shape[-1], 1)
ys = to_np(dbz_cross.coords["vertical"])
dbz_contours = ax_cross.contourf(xs,
                                 ys,
                                 to_np(dbz_cross_filled),
                                 levels=dbz_levels,
                                 cmap=dbz_map,
                                 norm=dbz_norm,
                                 extend="max")


# Make the contour plot
#xとyも2次元である必要がある
#何故か上空に行くと矢印が小さくなる
o=np.zeros(37200).reshape(100,372)
x=xs[np.newaxis,:]+o
y=ys[:,np.newaxis]+o
print(x.shape,y.shape,to_np(wspd_cross[1,:,:]).shape,to_np(wa_cross[:,:]).shape)
wspd_contours = ax_cross.quiver(x[::10,::30],y[::10,::30],to_np(wspd_cross[1,::10,::30]), to_np(wa_cross[::10,::30]*10))


# Add the color bar
cb_dbz = fig.colorbar(dbz_contours, ax=ax_cross)
cb_dbz.ax.tick_params(labelsize=8)

# Fill in the mountain area
ht_fill = ax_cross.fill_between(xs, 0, to_np(ter_line),
                                facecolor="saddlebrown")

# Set the x-ticks to use latitude and longitude labels
coord_pairs = to_np(dbz_cross.coords["xy_loc"])
x_ticks = np.arange(coord_pairs.shape[0])
x_labels = [pair.latlon_str() for pair in to_np(coord_pairs)]

# Set the desired number of x ticks below
num_ticks = 5
thin = int((len(x_ticks) / num_ticks) + .5)
ax_cross.set_xticks(x_ticks[::thin])
ax_cross.set_xticklabels(x_labels[::thin], rotation=45, fontsize=8)

# Set the x-axis and  y-axis labels
ax_cross.set_xlabel("Latitude, Longitude", fontsize=12)
ax_cross.set_ylabel("Height (m)", fontsize=12)

# Add a title
ax_cross.set_title("Cross-Section of Reflectivity (dBZ)", {"fontsize" : 14})

fig.savefig("test", dpi=500, bbox_inches='tight', pad_inches=0.1)
pyplot.show()
