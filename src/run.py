import readMap as rm
import numpy as np
import aStar


def run():
    boundaries = np.array([-73.59, -73.55, 45.49, 45.53], dtype=float)
    grid_size = 0.002
    threshold = 60
    crim_data = rm.manipulate_data(boundaries, grid_size, threshold)
    rm.show_grids(crim_data, boundaries, grid_size, threshold)
    # print(crim_data)
    path = np.array(aStar.astar_search(crim_data, [0, 0], [20, 20]), dtype=float)

    print(path)

    xs, ys = rm.get_tickers(boundaries, grid_size)
    x_axis = np.array(path[:, 1], dtype=float)
    y_axis = np.array(path[:, 0], dtype=float)
    for i in range(len(x_axis)):
        x_axis[i] = xs[int(x_axis[i])]
    for i in range(len(y_axis)):
        y_axis[i] = ys[int(y_axis[i])]

    rm.show_grids(crim_data, boundaries, grid_size, threshold, path=[x_axis,y_axis])


run()

