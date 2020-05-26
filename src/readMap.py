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
crim_data, xedges, yedges = np.histogram2d(Y, X, [y_axis, x_axis])
# Compute the average
mean = np.mean(crim_data)
# Compute the standard deviation
std = np.std(crim_data)
print(mean, std)
# Covert the 2d array to a linear array, and sort in descending order
linear_crim = np.sort(crim_data.flatten())[::-1]
# Get the value compouted with threshold
threshold = 75
thre_ele = linear_crim[int(np.floor(len(linear_crim) * (100-threshold) / 100 -1))]

# Transfer the elements to binary value according to the threshokld value
crim_data_binary = (crim_data >= thre_ele).astype(int)
#plt.pcolor(x_axis, y_axis, crim_data_binary)
plt.imshow(crim_data_binary, extent=[X0, X1, Y0, Y1], origin='lower')
#x_ticks = np.arange(X0, X1 + grid_size * 5/2, grid_size*5)
#y_ticks = np.arange(Y0, Y1 + grid_size * 5/2, grid_size*5)
#plt.xticks(x_axis)
#plt.yticks(y_axis)
#plt.grid(b= True, which='both')

grid_path = '../images/grids/grids_size' + str(grid_size)+ '_threshold' +str(threshold/100) + '.png'
plt.savefig(grid_path)
plt.show()

'''
# Combine X and Y
A = np.array(list(zip(X, Y)))
# Sort the array according to the first colomn
B = A[np.lexsort(A[:,::-1].T)]

D = np.zeros(400).reshape(20, 20)
for i in range(size):
    for j in range(len(x_axis) - 1):
        if B[i][0] >= x_axis[j] and B[i][0] <= x_axis[j+1]:
            for k in range(len(y_axis)-1):
                if B[i][1] >= y_axis[k] and B[i][1] <= y_axis[k+1]:
                    D[j][k] += 1
print(D)
'''
