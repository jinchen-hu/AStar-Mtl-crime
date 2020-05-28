import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np


def read_map():
    # Define the path of shape files
    shpFilePath='../shape_file/crime_dt.shp'
    # Read the data of shape file as GeoDataFrame list, and extract geometry object only
    mtr_data = gpd.GeoDataFrame.from_file(shpFilePath).geometry
    # Get the length of the list
    total = len(mtr_data)
    # X stores x-axis data, Y stores y-axis data
    X = mtr_data.x
    Y = mtr_data.y
    return X, Y, total


def get_tickers(boundaries, grid_size=0.002):
    # Compute grids, in case the grid_size cannot be divided evenly, plus half grad size is needed
    x_axis = np.arange(boundaries[0], boundaries[1] + grid_size / 2, grid_size, dtype=float)
    y_axis = np.arange(boundaries[2], boundaries[3] + grid_size / 2, grid_size, dtype=float)
    return x_axis, y_axis


def manipulate_data(boundaries, grid_size=0.002, threshold = 0.9):
    X, Y, total = read_map()
    x_axis, y_axis = get_tickers(boundaries, grid_size)
    # Create a 2d histogram to collect criminals
    crim_data, _, _ = np.histogram2d(Y, X, bins=[y_axis, x_axis])
    # Compute the average
    mean = np.mean(crim_data)
    # Compute the standard deviation
    std = np.std(crim_data)
    # Covert the 2d array to a linear array, and sort in descending order
    linear_crim = np.sort(crim_data.flatten())[::-1]
    # Get the value compouted with threshold
    thre_value = linear_crim[int(np.floor(len(linear_crim) * (100 - threshold) / 100 -1))]
    # Transfer the elements to binary value according to the threshokld value
    crim_data_binary = (crim_data >= thre_value).astype(int)
    return crim_data_binary


def show_grids(crim_data_binary, boundaries, grid_size, threshold, path=None):

    #plt.imshow(crim_data_binary, extent=boundaries, aspect='auto', origin='lower')
    x_ticks, y_ticks = get_tickers(boundaries, grid_size)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    plt.pcolor(x_ticks, y_ticks, crim_data_binary)
    plt.grid(b= True, axis='both', which='both')
    grid_path = '../images/grids/grids_size' + str(grid_size) + '_threshold' + str(threshold / 100) + '.png'
    if path:
        # xs = np.array(path[:, 1], dtype=float)
        # ys = np.array(path[:, 0], dtype=float)
        # for i in range(len(xs)):
        #     xs[i] = x_ticks[int(xs)]
        # for i in range(len(ys)):
        #     ys[i] = y_ticks[int(ys)]
        plt.plot(path[0], path[1])
        grid_path = '../images/paths/grids_size'+ str(grid_size) + '_threshold' + str(threshold / 100) + '.png'
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
