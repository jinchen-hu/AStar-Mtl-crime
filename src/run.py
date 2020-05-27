import readMap as rm
import numpy as np
import aStar

def run():
    boundaries = np.array([-73.59, -73.55, 45.49, 45.53])
    grid_size = 0.002
    threshold = 75
    crim_data = rm.manipulate_data(boundaries, grid_size, threshold)
    rm.show_grids(crim_data, boundaries, grid_size, threshold)
    print(crim_data)
    path = aStar.astar_search(crim_data, (0, 0), (200,200))
    print(path)


run()

