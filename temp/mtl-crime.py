# -------------------------------------------------------
# Project 1
# Written by:
# An Nguyen - 40087621 For COMP 6721 Section FJ – Fall 2019
# Dung Do - 40109919 For COMP 6721 Section FI – Fall 2019
# --------------------------------------------------------

import numpy as np
import search
import map
import signal


def signal_handler():
    raise Exception("Time is up. The optimal path is not found!")


def run(gridsize, threshold, method):
    X0, Y0 = -73.59, 45.49
    X1, Y1 = -73.55, 45.53
    gridsize = gridsize

    long_tickers, lat_tickers = map.get_tickers(X0, X1, Y0, Y1, gridsize)

    map_left = long_tickers.min()
    map_right = long_tickers.max()
    map_bottom = lat_tickers.min()
    map_top = lat_tickers.max()

    bottom_left = (map_left, map_bottom)
    top_right = (map_right, map_top)

    crime_dt = map.read_geo_data("Shape/crime_dt.shp")
    crime_hist, crime_threshold, mean, std_dev = map.calculate_map(bottom_left=bottom_left,
                                                                   top_right=top_right,
                                                                   grid_size=gridsize,
                                                                   data_points=crime_dt,
                                                                   threshold=threshold)

    map.draw(crime_threshold, bottom_left=bottom_left, top_right=top_right, route=None)

    height, width = crime_threshold.shape
    points_in_grid = []

    try:
        # Set time limit to 10 seconds
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(10)
        points_in_grid = search.search(crime_threshold, (0, width), (height, 0), method=method)
    except Exception as msg:
        print("Time is up. The optimal path is not found!")

    if len(points_in_grid) == 0:
        map.draw(crime_threshold, bottom_left=bottom_left, top_right=top_right, route=None)
    else:
        signal.alarm(0)
        route = np.column_stack((long_tickers[points_in_grid[:, 1]], lat_tickers[points_in_grid[:, 0]]))
        route[0] = np.array([X1, Y0])
        if route[-1][1] > 45.53:
            route[-1] = np.array([X0, Y1])
        map.draw(crime_threshold, bottom_left=bottom_left, top_right=top_right, route=route)


run(0.002, 75, 'a')