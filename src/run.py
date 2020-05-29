# -----------------------------------------------------
# Assignment 1
# Written by Jinchen Hu - 40080398
# For COMP 472 Section ABIX - Summer 2020
# -----------------------------------------------------

import readMap as rm
import numpy as np
import aStar
import signal


# Define a timeout exception
class TimeOutException(Exception):
    pass


# Define a exception handler
def signal_handler(signum, frame):
    raise TimeOutException('Time is up. The optimal path is not found.')


# Prompt the user input the grid size
def read_grid_size():
    while True:
        grid_size = eval(input('Please enter the grid size ( <= 0.002 is recommended): '))
        if 0 < grid_size <= 0.04:
            return grid_size
        else:
            print('Invalid input! ')


# Prompt the user input threshold
def read_threshold():
    while True:
        threshold = eval(input('Please enter the threshoud ( 0~100 ): '))
        if 0 < threshold < 100:
            return threshold
        else:
            print('Invalid input! ')


# Prompt the user enter the starting point and end point
def read_start_end(boundaries, grid_size):
    while True:
        print('Please enter the starting point and destination')
        print('Input Format:  Longitude (-73.59~-73.55), Latitude (45.49~45.53)')

        # Get the start point
        def get_start():
            while True:
                start = eval(input('Please enter the starting point: '))
                if -73.59 <= start[0] <= -73.55 and 45.49 <= start[1] <= 45.53:
                    return start
                else:
                    print('The point you input is out of the boundary')
        # Get the end point

        def get_end():
            while True:
                end = eval(input('Please enter the destination: '))
                if -73.59 <= end[0] <= -73.55 and 45.49 <= end[1] <= 45.53:
                    return end
                else:
                    print('The point you input is out of the boundary')

        start_point, end_point = get_start(), get_end()

        long, lat = rm.get_tickers(boundaries, grid_size)
        # Traverse the long array and lat array, find the proper indices
        # for starting point and end point respectively
        h0, h1, w0, w1, llat, llong = 0, 0, 0, 0, len(lat), len(long)
        if start_point[1] == round(lat[llat-1], 10):
            h0 = llat-1
        else:
            for h0 in range(llat-1):
                if round(lat[h0], 10) <= start_point[1] < round(lat[h0+1], 10):
                    break

        if end_point[1] == round(lat[llat-1], 10):
            h1 = llat-1
        else:
            for h1 in range(llat-1):
                if round(lat[h1], 10) <= end_point[1] < round(lat[h1+1], 10):
                    break

        if start_point[0] == round(long[llong-1],10):
            w0 = llong-1
        else:
            for w0 in range(llong-1):
                if round(long[w0], 10) <= start_point[0] < round(long[w0+1], 10):
                    break

        if end_point[0] == round(long[llong-1], 10):
            w1 = llong-1
        else:
            for w1 in range(llong - 1):
                if round(long[w1], 10) <= end_point[0] < round(long[w1+1], 10):
                    break

        if h0 == h1 and w0 == w1:
            print('Starting point is same as destination. Please input again')
            continue
        else:
            print('\n\n')
            print('The starting point and end point you chose (if not a intersection point, change it to the lowest point): ')
            print(str([round(long[w0],10), round(lat[h0], 10)]) + ' ---> ' + str( [round(long[w1], 10),round(lat[h1], 10)]))
            return [h0, w0], [h1, w1]


def run():
    print('----------------------------------------------Welcome to FIND OPTIMAL PATH!---------------------------------------------------\n')
    print('The application will give you the optimal path reaching the destination from starting position, which avoids high-risk areas\n')
    print('------------------------------------------------------------------------------------------------------------------------------')
    print('\n\n\n')

    boundaries = np.array([-73.59, -73.55, 45.49, 45.53], dtype=float)
    grid_size = read_grid_size()
    print('\n')
    threshold = read_threshold()
    crim_data = rm.manipulate_data(boundaries, grid_size, threshold)
    print('The map will show up immediately')
    rm.show_grids(crim_data, boundaries, grid_size, threshold)
    print('\n\n')
    # -73.59, 45.49, -73.55, 45.53
    print('***********************************************************\n')

    start_index, end_index = read_start_end(boundaries, grid_size)
    path = []

    try:
        # Set the signal, and time limit to 10s
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(10)

        path = np.array(aStar.astar_search(crim_data, start_index, end_index), dtype=float)
    except TimeOutException as message:
        print('Time us up. The optimal path is not found')

    if len(path) > 0:
        # Cancel the signal
        signal.alarm(0)
        xs, ys = rm.get_tickers(boundaries, grid_size)
        x_axis = np.array(path[:, 1], dtype=float)
        y_axis = np.array(path[:, 0], dtype=float)
        for i in range(len(x_axis)):
            x_axis[i] = xs[int(x_axis[i])]
        for i in range(len(y_axis)):
            y_axis[i] = ys[int(y_axis[i])]

        rm.show_grids(crim_data, boundaries, grid_size, threshold, path=[x_axis,y_axis])
    print('\n\n###########################################################################################')
    print('\n### Thanks very much for using our application. The program will terminate right now ###')


run()