# -------------------------------------------------------
# Project 1
# Written by Dung Do - 40109919
# For COMP 6721 Section FI – Fall 2019
# -------------------------------------------------------

# Module to define heuristic function(s)

import sys
import math


def manhattan_distance(city_map, current, goal):
    """
    The heuristic function based on the idea of Manhattan distance.
    Instead of go horizontally and vertically, we go along diagonal lines if possible.
    The cost of the diagonal move is 1.5 weighted.
    In details, we go straight until we find a diagonal line to go directly to the goal.
    It is optimistic, ignores the crime areas and assumes that we can get to the end point with the shortest path.
    :param city_map: The map with crime block
    :param current: current position coordinate (row, col)
    :param goal: goal coordinate (row, col)
    :return: return the evaluated heuristic value of current position
    """

    height_, width_ = city_map.shape

    row_cur, col_cur = current
    row_goal, col_goal = goal

    # We should penalize the points outside the map, their heuristic values should be MAX_INT
    if col_cur < 0 or col_goal < 0 or col_cur > width_ or col_goal > width_:
        return sys.maxsize
    if row_cur < 0 or row_goal < 0 or row_cur > height_ or row_goal > height_:
        return sys.maxsize

    horizontal_step = math.fabs(col_goal - col_cur)
    vertical_step = math.fabs(row_goal - row_cur)

    # Without losing generality, we assume vertical distance is always shorter than or equal to horizontal distance
    if vertical_step > horizontal_step:
        temp = vertical_step
        vertical_step = horizontal_step
        horizontal_step = temp

    # Then the ideal route cost should be calculated as the sum of 2 parts:
    return vertical_step * 1.5 + (horizontal_step - vertical_step)