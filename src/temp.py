from temp import aStar
import numpy as np
n1 = aStar.Node([1, 1])
n1.fn = 4
n2 = aStar.Node([2, 1])
n2.fn = 1
n3 = aStar.Node([3, 1])
n3.fn = 3
n4 = aStar.Node([4, 1])
n4.fn = 2
n5 = aStar.Node([5, 1])
n5.fn = 1


class Node(object):
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]
        self.coord = coord
        self.isclose = False
        self.isopen = False
        self.parent = None
        self.hn = 0
        self.gn = 0
        self.fn = 0
    def __str__(self):
        return str([self.x, self.y])


def children(point, grid):
    x, y = point.point
    links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]]
    return [link for link in links if link.value != '%']

start = [9,6]
goal = [20,20]
grid = np.array([[Node([y,x]) for x in range(21)] for y in range(21)])
goal_point = grid[goal[0]][goal[1]]
current = grid[start[0]][start[1]]
current.isclose = True
modf = grid[start[0]][start[1]]
print(goal_point)
print(modf.isclose)

if not grid[3][3]:
    print(66666)

print(type(grid))
print(type(grid)== np.ndarray)