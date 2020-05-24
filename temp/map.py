# -------------------------------------------------------
# Project 1
# Wrriten by An Nguyen - 40087621 - For COMP 6721 Section FJ - Fall 2019
# Written by Dung Do - 40109919 - For COMP 6721 Section FI – Fall 2019
# -------------------------------------------------------

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt


def get_tickers(X0, X1, Y0, Y1, gridsize):
    long_arr = np.arange(X0, X1 + gridsize * 0.9, gridsize)
    lat_arr = np.arange(Y0, Y1 + gridsize * 0.9, gridsize)
    return long_arr, lat_arr


def read_geo_data(input_file):
    geo_dt = gpd.read_file(input_file)
    return geo_dt


def calculate_map(bottom_left, top_right, grid_size=0.002, data_points=None,
                  threshold=0):
    """
        Calculate crime map histogram, mean and standard deviation
        :param bottom_left: bottom left coordinate of the map
        :param top_right: top right coordinate of the map
        :param grid_size: length of a dimension of a cell
        :param data_points: the list of data point representing crime
        :param threshold: threshold to be applied to the crime areas
        :return: (histogram, mean, standard_deviation)
        """

    x0, y0 = bottom_left
    x1, y1 = top_right

    # Create the grid with 2 dimensions
    long = np.arange(x0, x1 + grid_size / 2, grid_size)
    lat = np.arange(y0, y1 + grid_size / 2, grid_size)

    # Separate the coordinates of crime points into 2 vectors to create a histogram
    X = data_points.geometry.x
    Y = data_points.geometry.y
    hist, xedges, yedges = np.histogram2d(Y, X, bins=[lat, long])
    # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Convert from percentage threshold to number threshold
    crime_array = hist.flatten()
    crime_array = -np.sort(-crime_array)
    threshold_index = int(np.size(crime_array) - (np.size(crime_array) * threshold / 100))
    threshold_value = crime_array.item(threshold_index)
    if threshold_value == 0:
        threshold_value = crime_array[crime_array > 0].min()

    # Flatten the histogram values with threshold, this means the histogram only contain values in {0, 1}
    hist_flat = np.copy(hist)
    hist_flat[hist_flat <= threshold_value] = 0
    hist_flat[hist_flat > threshold_value] = 1

    mean_ = np.mean(hist)
    std_dev_ = np.std(hist)

    print("Mean: {0:.4f}".format(mean_))
    print("Standard deviation: {0:.4f}".format(std_dev_))
    print("Total number in each grid:")
    print(hist)

    return hist, hist_flat, mean_, std_dev_


def draw(hist, bottom_left, top_right, route=None):
    """
    Draw the map with block areas
    :param hist: the histogram of crime rate on map
    :param bottom_left: bottom left coordinate in format (col, row)
    :param top_right: top right coordinate in format (col, row)
    :param route: a route on map. Default value is None
    :return: None
    """
    x0, y0 = bottom_left
    x1, y1 = top_right

    # Separate the coordinates of crime points into 2 vectors to create a histogram
    extent = [x0, x1, y0, y1]

    plt.imshow(hist, origin='lower', extent=extent, interpolation='nearest', aspect='auto')
    if route is None:
        plt.show()
    else:
        long_vec, lat_vec = route.T
        plt.plot(long_vec, lat_vec)
        plt.show()