# -------------------------------------------------------
# Project 1
# Written by Dung Do - 40109919
# For COMP 6721 Section FI – Fall 2019
# -------------------------------------------------------

# Module for searching path functions

import math
import numpy as np
import sys
import heuristic
import time


class Node:
    """A node class representing a position on map for A* Algorithm, similar to linked list"""

    def __init__(self, prev=None, row=None, col=None):
        self.prev = prev
        self.row = row
        self.col = col
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.col, self.row))

    def __str__(self):
        return "({0}, {1})".format(self.row, self.col)


def mountain_climb(city_map, start, end):
    """
    Perform searching for a possible path from start point to end point using algorithm A.
    This searching function considers both cost and heuristic values.
    :param city_map: the map on which we need to search for a path on.
    :param start: starting position, type Node
    :param end: goal position, type Node
    :return: list of moves from start to end
    """

    start_time = time.time()

    start_row, start_col = start
    start_node = Node(None, start_row, start_col)

    end_row, end_col = end
    end_node = Node(None, end_row, end_col)

    path = np.array([start_node.row, start_node.col])

    total_cost = 0
    current_node = start_node
    prev_node = None

    while current_node != end_node:

        neighbors = find_all_possible_moves(city_map, set(), current_node, end_node)
        eval_neighbors = []

        if len(neighbors) > 0:
            #  If we found possible moves
            for child_node, cost in neighbors:
                child_node.g = current_node.g + cost
                child_node.h = heuristic.manhattan_distance(city_map, (child_node.row, child_node.col), end)
                eval_neighbors.insert(0, child_node)

            eval_neighbors.sort(key=lambda item: item.h)

            chosen = eval_neighbors[0]
            path = np.vstack((np.array([chosen.row, chosen.col]), path))
            current_node = chosen
            total_cost = total_cost + chosen.g

        else:
            # If there is no possible moves
            break

    if current_node == end_node:
        end_time = time.time()
        print("A path was found in {0:.4f} seconds".format(end_time - start_time))
        print("Cost: {0:.1f}".format(total_cost))
    else:
        print("Due to blocks, no path is found. Please change the map and try again.")

    return path


def search(crime_map, start, end, method="a"):
    """
    Returns a list of coordinate of points in the  path from the given start to the given end.
    By default, the search algorithm used is best-first. Pass method="a" to use Algorithm A.
    :param crime_map: numpy array of the city crime map
    :param start: starting point of the path
    :param end: end point of the path
    :param method: Pass "a" to use Algorithm A. Otherwise, best-first is used.
    :return: a numpy array in which a row is a coordinate of a point on the path found. Empty if no path found.
    """

    start_time = time.time()

    open_list = []
    closed_list = set()

    start_row, start_col = start
    start_node = Node(None, start_row, start_col)

    end_row, end_col = end
    end_node = Node(None, end_row, end_col)

    if not valid_goal(crime_map, end):
        print("Due to blocks, no path is found. Please change the map and try again.")
        return []

    # Initialize openlist with the start node
    open_list.append(start_node)

    # Loop until find the end
    while len(open_list) > 0:

        current_node = open_list.pop(0)
        closed_list.add(current_node)

        # Found the goal
        if current_node == end_node:
            end_time = time.time()
            print("A path was found in {0:.4f} seconds".format(end_time - start_time))
            print("Cost: {0:.1f}".format(current_node.g))
            return get_reconstructed_path(current_node)

        # Generate children nodes
        children = find_all_possible_moves(crime_map, closed_list, current_node, end_node)

        for child_node, cost in children:
            # Create the f, g, and h values
            child_node.g = current_node.g + cost
            child_node.h = heuristic.manhattan_distance(crime_map, (child_node.row, child_node.col), end)

            # If using A algorithm then calculate f = g + h
            if method == "a":
                child_node.f = child_node.g + child_node.h
            open_list.insert(0, child_node)

        # If using A algorithm then sort open list with f value
        if method == "a":
            open_list.sort(key=lambda item: item.f)  # TODO time consuming
        # If using best-first then sort open list with h
        else:
            open_list.sort(key=lambda item: item.h)

    print("Due to blocks, no path is found. Please change the map and try again.")
    return []


def get_reconstructed_path(from_node):
    """
    This structure is similar to linked list since we only need to keep the pointer to the first node.
    :param from_node: The node that we start backtracking
    :return: The path in format of a numpy array, each row is the coordinate of a point.
    """

    path = np.array([from_node.row, from_node.col])

    current = Node(from_node.prev, from_node.row, from_node.col)
    while current.prev is not None:
        prev = current.prev
        current = Node(prev.prev, prev.row, prev.col)
        path = np.vstack((np.array([prev.row, prev.col]), path))

    return path


def find_all_possible_moves(city_map, excluded_nodes, current_node, end_node):
    """
    Find all possible moves from current position. The previous position is excluded because we do not want to go back.
    All position params are in format (row, col).
    We list out all the neighbors and evaluate the cost of the move to these neighbors.
    A neighbor is chosen if the cost of the move to that node is not infinity (infinity is MAX_INT here by convention)
    By evaluating cost of moves, we do 2 things at a times, find neighbors and cost of moves to them.them
    :param city_map: the crime city map on which we need to find a path
    :param excluded_nodes: the visited positions on map
    :param current_node: current position on map
    :param end_node: end position
    :return: list of all possible moves from current position
    """
    result = []

    row_cur = current_node.row
    col_cur = current_node.col

    left = Node(current_node, row_cur, col_cur - 1)
    left_cost = move_cost(city_map, current_node, left, end_node)

    right = Node(current_node, row_cur, col_cur + 1)
    right_cost = move_cost(city_map, current_node, right, end_node)

    up = Node(current_node, row_cur + 1, col_cur)
    up_cost = move_cost(city_map, current_node, up, end_node)

    down = Node(current_node, row_cur - 1, col_cur)
    down_cost = move_cost(city_map, current_node, down, end_node)

    up_left = Node(current_node, row_cur + 1, col_cur - 1)
    up_left_cost = move_cost(city_map, current_node, up_left, end_node)

    up_right = Node(current_node, row_cur + 1, col_cur + 1)
    up_right_cost = move_cost(city_map, current_node, up_right, end_node)

    down_left = Node(current_node, row_cur - 1, col_cur - 1)
    down_left_cost = move_cost(city_map, current_node, down_left, end_node)

    down_right = Node(current_node, row_cur - 1, col_cur + 1)
    down_right_cost = move_cost(city_map, current_node, down_right, end_node)

    if left not in excluded_nodes and left_cost < sys.maxsize:
        result.append((left, left_cost))

    if right not in excluded_nodes and right_cost < sys.maxsize:
        result.append((right, right_cost))

    if up not in excluded_nodes and up_cost < sys.maxsize:
        result.append((up, up_cost))

    if down not in excluded_nodes and down_cost < sys.maxsize:
        result.append((down, down_cost))

    if up_left not in excluded_nodes and up_left_cost < sys.maxsize:
        result.append((up_left, up_left_cost))

    if up_right not in excluded_nodes and up_right_cost < sys.maxsize:
        result.append((up_right, up_right_cost))

    if down_left not in excluded_nodes and down_left_cost < sys.maxsize:
        result.append((down_left, down_left_cost))

    if down_right not in excluded_nodes and down_right_cost < sys.maxsize:
        result.append((down_right, down_right_cost))

    return result


def move_cost(city_map, from_node, to_node, end_node):
    """
    Calculate cost of a move. All position params are in format (row, col).
    If the there is no move to to_node, the cost is infinity, which is sys.maxsize in python.
    :param city_map: the crime city map on which we need to find a path
    :param from_node: starting point of the move
    :param to_node: end point of the move
    :param end_node: goal point
    :return: cost of the move
    """

    height_, width_ = city_map.shape

    row_cur = from_node.row
    col_cur = from_node.col

    row_next = to_node.row
    col_next = to_node.col

    row_end = end_node.row
    col_end = end_node.col

    # if the end point is out of the map, return infinity
    if col_cur < 0 or col_next < 0 or col_cur > width_ or col_next > width_:
        return sys.maxsize
    if row_cur < 0 or row_next < 0 or row_cur > height_ or row_next > height_:
        return sys.maxsize

    horizontal_step = col_next - col_cur
    vertical_step = row_next - row_cur

    # if the distance is longer than 1, return infinity
    if math.fabs(horizontal_step) > 1 or math.fabs(vertical_step) > 1:
        return sys.maxsize

    # if the to_pos is not the goal pos, the cost of a move to the edge is mark as infinity
    if to_node != end_node:
        if col_next == 0 or row_next == 0 or col_next == width_ or row_next == height_:
            return sys.maxsize

    # Diagonal move
    if horizontal_step != 0 and vertical_step != 0:
        checking_col = col_cur if horizontal_step > 0 else col_cur - 1
        checking_row = row_cur if vertical_step > 0 else row_cur - 1
        return 1.5 if city_map[checking_row, checking_col] == 0 else sys.maxsize

    # Vertical move
    if horizontal_step == 0:
        checking_row = row_cur
        # Move up on numpy array but down on real map
        if vertical_step < 0:
            checking_row = row_cur - 1
        # Move down on numpy array but up on real map
        if vertical_step > 0:
            checking_row = row_cur
        # Not blocked both sides
        if city_map[checking_row, col_cur - 1] == 0 and city_map[checking_row, col_cur] == 0:
            return 1
        # One side blocked
        if city_map[checking_row, col_cur - 1] == 0 or city_map[checking_row, col_cur] == 0:
            return 1.3
        # Tow sides blocked
        return sys.maxsize

    # Horizontal move
    if vertical_step == 0:
        checking_col = col_cur
        # Move left
        if horizontal_step < 0:
            checking_col = col_cur - 1
        # Move right
        if horizontal_step > 0:
            checking_col = col_cur

        # Not blocked both sides
        if city_map[row_cur - 1, checking_col] == 0 and city_map[row_cur, checking_col] == 0:
            return 1
        # One side blocked
        if city_map[row_cur - 1, checking_col] == 0 or city_map[row_cur, checking_col] == 0:
            return 1.3
            # Tow sides blocked
        return sys.maxsize

    return sys.maxsize


def valid_goal(city_map, goal):
    row, col = goal
    height_, width_ = city_map.shape

    # if the end point is out of the map, return infinity
    if col < 0 or row < 0 or col > width_ or row > height_:
        return False

    # bottom edge
    if row == 0:
        if col == 0:
            return city_map[0, 0] == 0
        if col == width_:
            return city_map[0, width_ - 1] == 0
        return city_map[0, col - 1] == 0 or city_map[0, col] == 0

    # top edge
    if row == height_:
        if col == 0:
            return city_map[height_ - 1, 0] == 0
        if col == width_:
            return city_map[height_ - 1, width_ - 1] == 0
        return city_map[height_ - 1, col - 1] == 0 or city_map[height_ - 1, col] == 0

    # left edge
    if col == 0:
        return city_map[row - 1, 0] == 0 or city_map[row, 0] == 0

    # right edge
    if col == width_:
        return city_map[row - 1, width_ - 1] == 0 or city_map[row, width_ - 1] == 0

    # internal
    return city_map[row - 1, col - 1] == 0 or city_map[row, col - 1] == 0 \
           or city_map[row - 1, col] == 0 or city_map[row, col] == 0