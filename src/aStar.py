
''' Pseudo-code of A*
    open, close = [], []
    open.add(starting_point)
    while open:
        open.sort() in descending order as fn
        current = open[0]
        open.remove(current)
        close.add(current)
        loop 8 adjacent/child points :
            if not in close && reachable
                if not in open
                    child.setParent(current)
                    child.fn = child.gn + child.hn
                    open.add(child)
                    open.sort()
                if in open
                    compute child.fn
                    if child.gn < open[child].gn
                        child.fn = child.gn + child.hn
                        child.parent = current
                        open.add(child)
                        open.sort()
        if current == des
            return path = des.parent.parent....
        if timeout
            return false
    return false
'''


# Create a Linked list object
class Node(object):
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]
        self.coord = coord
        self.close = False
        self.open = False
        self.parent = None
        self.hn = 0
        self.gn = 0
        self.fn = 0

    def is_equal(self, pt):
        return self.x == pt.x and self.y == pt.y

    def __str__(self):
        return str([self.x, self.y])

    # Estimate the hn by computing the shortest path regardless of block areas
    def get_hn(self, goal):
        return int(((goal[0]-self.x) ** 2 + (goal[1]-self.y) ** 2) ** 0.5)


# Use indices of start point and end point, since it's easy to compute hn
# more importantly, avoid the convenience of unevenly distribution
def astar_search(crim_data, start, goal):

    width, height = crim_data.shape
    open_set = set()
    close_set = set()
    current = Node(start)
    #goal_node = Node(goal)
    open_set.add(current)
    current.open = True

    while open_set:
        # Get the point with smallest fn as current node
        current = min(open_set, key=lambda n: n.fn)
        if current.coord == goal:
            return retrace_path(current)
        # Remove the current node from open set
        open_set.remove(current)
        current.open = False
        # Add it to close set
        current.close = True
        close_set.add(current)

        x, y = current.x, current.y
        up, down, left, right = y + 1, y - 1, x - 1, x + 1

        def if_reachable(current_node, next_node):
            # invalid condition: in close list, out of map, boundary edges
            if next_node.close or next_node.x < 0 or next_node.x > width or next_node.y < 0 or next_node.y > height \
                    or next_node.x == current_node.x == 0 or next_node.x == current_node.x == width \
                    or next_node.y == current_node.y == 0 or next_node.y == current_node.y == height:
                return False

        # Compute the path weight moving to the next point, return false if the path will cross through block areas
        def up_gn(pt):
            if crim_data[pt.x][pt.y - 1] == 0 and crim_data[pt.x][pt.y] == 0:
                return 1
            elif crim_data[pt.x][pt.y - 1] == 0 or crim_data[pt.x][pt.y] == 0:
                return 1.3
            else:
                return False

        def upright_gn(pt):
            return 1.5 if crim_data[pt.x][pt.y] == 0 else False

        def right_gn(pt):
            if crim_data[pt.x][pt.y] == 0 and crim_data[pt.x - 1][pt.y] == 0:
                return 1
            elif crim_data[pt.x][pt.y] == 0 or crim_data[pt.x - 1][pt.y] == 0:
                return 1.3
            else:
                return False

        def downright_gn(pt):
            return 1.5 if crim_data[pt.x - 1][pt.y] == 0 else False

        def down_gn(pt):
            if crim_data[pt.x - 1][pt.y] == 0 and crim_data[pt.x - 1][pt.y - 1] == 0:
                return 1
            elif crim_data[pt.x - 1][pt.y] == 0 or crim_data[pt.x - 1][pt.y - 1] == 0:
                return 1.3
            else:
                return False

        def downleft_gn(pt):
            return 1.5 if crim_data[pt.x - 1][pt.y - 1] == 0 else False

        def left_gn(pt):
            if crim_data[pt.x][pt.y - 1] == 0 and crim_data[pt.x - 1][pt.y - 1] == 0:
                return 1
            elif crim_data[pt.x][pt.y - 1] == 0 or crim_data[pt.x - 1][pt.y - 1] == 0:
                return 1.3
            else:
                return False

        def upleft_gn(pt):
            return 1.5 if crim_data[pt.x][pt.y - 1] == 0 else False

        def if_add_open(current_node, pt, g_path):
            # If pt is in the open list, compare the new gn with stored gn
            if pt.open:
                new_g = g_path + current_node.gn
                # If current gn is greater, update gn and fn with new gn
                if pt.gn > new_g:
                    pt.gn = new_g
                    pt.hn = pt.gn + pt.get_hn(goal)
                    # set parent node to current point
                    pt.parent = current_node
            # If it's not in the open list, add it in the open list
            else:
                # Compute gn, hn, fn
                pt.hn = pt.gn + pt.get_hn(goal)
                pt.gn = g_path + current_node.gn
                pt.fn = pt.gn + pt.hn
                # Set open to true
                pt.open = True
                # Set parent node to current point
                pt.parent = current_node
                # Add it to the open list
                open_set.add(pt)

        # Literate the children nodes, and determine whether add them
        # in the open set
        up_point = Node([x, up])
        if if_reachable(current, up_point):
            g = up_gn(current)
            # If we can reach this point
            if g:
                if_add_open(current, up_point, g)

        up_right = Node([right, up])
        if if_reachable(current, up_right):
            g = upright_gn(current)
            # If we can reach this point
            if g:
                if_add_open(current, up_right, g)

        right_point = Node([right, y])
        if if_reachable(current, right_point):
            g = right_gn(current)
            # If we can reach this point
            if g:
                if_add_open(current, right_point, g)

        down_right = Node([right, down])
        if if_reachable(current, down_right):
            g = downright_gn(current)
            # If we can reach this point
            if g:
                if_add_open(current, down_right, g)

        down_point = Node([x, down])
        if if_reachable(current, down_point):
            g = down_gn(current)
            # If we can reach this point
            if g:
                if_add_open(current, down_point, g)

        down_left = Node([left, down])
        if if_reachable(current, down_left):
            g = downleft_gn(current)
            # If we can reach this point
            if g:
                if_add_open(current, down_left, g)

        left_point = Node([left, y])
        if if_reachable(current, left_point):
            g = left_gn(current)
            # If we can reach this point
            if g:
                if_add_open(current, left_point, g)

        up_left = Node([left, up])
        if if_reachable(current, up_left):
            g = upleft_gn(current)
            # If we can reach this point
            if g:
                if_add_open(current, up_left, g)
    return "sorry"

def retrace_path(current):
    # def parentgen(node):
    #     while node:
    #         yield node
    #         node = node.parent
    # path = [ele for ele in parentgen(node)]
    # path.reverse()
    # return path
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1]















