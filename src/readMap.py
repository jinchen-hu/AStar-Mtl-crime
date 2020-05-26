import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np

# Define the path of shape files
shpFilePath='../shape_file/crime_dt.shp'
# Read the data of shape file as GeoDataFrame list, and extract geometry object only
mtr_data = gpd.GeoDataFrame.from_file(shpFilePath).geometry
# Get the length of the list
size = len(mtr_data)
# X stores x-axis data, Y stores y-axis data
X = mtr_data.x
Y = mtr_data.y

# Define the range of map
grid_size = 0.002
X0, X1 = -73.59, -73.55
Y0, Y1 = 45.49, 45.53
# Compute grids, in case the grid_size cannot be divided evenly, plus half grad size is needed
x_axis = np.arange(X0, X1 + grid_size/2, grid_size)
y_axis = np.arange(Y0, Y1 + grid_size/2, grid_size)
# Create a 2d histogram to collect criminals
crim_data, x_edges, y_edges = np.histogram2d(Y, X, [y_axis, x_axis])
# Compute the average
mean = np.mean(crim_data)
# Compute the standard deviation
std = np.std(crim_data)
# Covert the 2d array to a linear array, and sort in descending order
linear_crim = np.sort(crim_data.flatten())[::-1]
#print(linear_crim)
# Get the threshold index
index = int(np.floor(len(linear_crim) * (100-75) / 100 -1))
var = linear_crim[index]
print(var)

arr = (crim_data >= var).astype(int)
print(arr)

plt.imshow(arr,origin='lower', extent=[X0, X1, Y0, Y1], interpolation='nearest', aspect='auto')
plt.show()








