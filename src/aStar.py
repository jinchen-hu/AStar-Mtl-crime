import time
''' Pseudo-code of A*
    open, close = [], []
    open.add(starting_point)
    while open:
        open.sort() in increasing order as fn
        current = open[0]
        open.remove(current)
        close.add(current)
        loop 8 adjacent/child points :
            if not in close && reachable
                if not in open
                    child.setParent(current)
                    child.fn = child.gn + child.hn
                    open.add(child)
                if in open
                    compute child.fn
                    if child.gn < open[child].gn
                        child.fn = child.gn + child.hn
                        child.parent = current
                        open.add(child)
        if current == des
            return path = des.parent.parent....
        if timeout
            return false
    return false
'''


# Create a Linked list object
class Node(object):
    def __init__(self, coord):
        self.h = coord[0]
        self.w = coord[1]
        self.coord = coord
        self.isclose = False
        self.isopen = False
        self.parent = None
        self.hn = 0
        self.gn = 0
        self.fn = 0

    def is_equal(self, pt):
        return self.h == pt.h and self.w == pt.w

    def __str__(self):
        return str([self.h, self.w])

    # Estimate the hn by computing the shortest path regardless of block areas
    def get_hn(self, goal):
        vert = abs(self.h-goal[0])
        hori = abs(self.w-goal[1])
        return min(vert, hori) * 1.5 + abs(vert-hori)


# Use indices of start point and end point, since it's easy to compute hn
# more importantly, avoid the convenience of unevenly distribution
def astar_search(crim_data, start, goal):
    start_time = time.time()

    def if_add_open(current_node, child_node, g_path):
        # If child is in the open list, compare the new gn with stored gn
        if child_node.isopen:
            new_g = g_path + current_node.gn
            # If current gn is greater, update gn and fn with new gn
            if child_node.gn > new_g:
                child_node.gn = new_g
                # compute the new fn
                child_node.fn = child_node.gn + child_node.get_hn(goal)
                # set parent node to current point
                child_node.parent = current_node
        # If it's not in the open list, add it in the open list
        else:
            # Compute gn, hn, fn
            child_node.hn = child_node.get_hn(goal)
            child_node.gn = g_path + current_node.gn
            child_node.fn = child_node.gn + child_node.hn
            # Set open to true
            # child_node.open_set = True
            # Set parent node to current point
            child_node.parent = current_node
            # Add it to the open list
            child_node.isopen = True
            open_set.add(child_node)

    # Compute the path weight moving to the next point, return false if the path will cross through block areas
    def up_gn(current_node):
        if crim_data[current_node.h][current_node.w-1] == 0 and crim_data[current_node.h][current_node.w] == 0:
            return 1
        elif crim_data[current_node.h][current_node.w-1] == 0 or crim_data[current_node.h][current_node.w] == 0:
            return 1.3
        else:
            return False

    def upright_gn(current_node):
        return 1.5 if crim_data[current_node.h][current_node.w] == 0 else False

    def right_gn(current_node):
        if crim_data[current_node.h][current_node.w] == 0 and crim_data[current_node.h-1][current_node.w] == 0:
            return 1
        elif crim_data[current_node.h][current_node.w] == 0 or crim_data[current_node.h-1][current_node.w] == 0:
            return 1.3
        else:
            return False

    def downright_gn(current_node):
        return 1.5 if crim_data[current_node.h-1][current_node.w] == 0 else False

    def down_gn(current_node):
        if crim_data[current_node.h-1][current_node.w-1] == 0 and \
                crim_data[current_node.h-1][current_node.w] == 0:
            return 1
        elif crim_data[current_node.h-1][current_node.w-1] == 0 or \
                crim_data[current_node.h-1][current_node.w] == 0:
            return 1.3
        else:
            return False

    def downleft_gn(current_node):
        return 1.5 if crim_data[current_node.h-1][current_node.w-1] == 0 else False

    def left_gn(current_node):
        if crim_data[current_node.h][current_node.w-1] == 0 and \
                crim_data[current_node.h-1][current_node.w-1] == 0:
            return 1
        elif crim_data[current_node.h][current_node.w-1] == 0 or \
                crim_data[current_node.h-1][current_node.w-1] == 0:
            return 1.3
        else:
            return False

    def upleft_gn(current_node):
        return 1.5 if crim_data[current_node.h][current_node.w-1] == 0 else False

    def if_reachable(current_node, next_node):
        # invalid condition: in close list, out of map, boundary edges
        if next_node.isclose or next_node.h == current_node.h == 0 \
                or next_node.h == current_node.h == width \
                or next_node.w == current_node.w == 0 \
                or next_node.w == current_node.w == height:
            return False
        else:
            return True

    def if_out(xx, yy):
        if xx < 0 or xx > height or yy < 0 or yy > width:
            return False
        else:
            return nodes[xx][yy]

    # Get the boundary asix
    height, width = crim_data.shape
    # Initialize all the nodes on the map
    nodes = [[Node([y, x]) for x in range(width+1)] for y in range(height+1)]
    # Create open set and close set
    open_set = set()
    close_set = set()
    goal_point = nodes[goal[0]][goal[1]]
    # Set start point as current node, and add it to open set
    current = nodes[start[0]][start[1]]
    current.isopen = True
    open_set.add(current)

    # Iterate the open set
    while open_set:
        # Get the point with smallest fn as current node
        current = min(open_set, key=lambda n: n.fn)
        # If reach to the destination, produce the path
        if current.is_equal(goal_point):
            end_time = time.time()
            print('Congratualations! The path is found in ' + str(end_time-start_time) + 's')
            return retrace_path(current)

        # Remove the current node from open set
        current.isopen = False
        open_set.remove(current)
        # Add it to close set
        current.isclose = True
        close_set.add(current)
        # Get the x-asix and y-asix of current node
        h, w = current.h, current.w
        # Get children nodes
        ''' if the child node is reachable
                if in open set
                    compare current gn with new gn
                    if current gn is greater
                        replace with new gn
                        set current node as parent
                    else ignore
                else
                    add it in open set
                    set current node as parent
            else ignore
        '''
        # 1. Check the validation of upper point
        up = if_out(h+1, w)
        if up:
            if if_reachable(current, up):
                g = up_gn(current)
                if g:
                    if_add_open(current, up, g)

        # 2. Check the validation of top right point
        up_right = if_out(h+1, w+1)
        if up_right:
            if if_reachable(current, up_right):
                g = upright_gn(current)
                if g:
                    if_add_open(current, up_right, g)

        # 3. Check the validation of right point
        right = if_out(h, w+1)
        if right:
            if if_reachable(current, right):
                g = right_gn(current)
                if g:
                    if_add_open(current, right, g)
        # 4. Check the validation of bottom right point
        down_right = if_out(h-1, w+1)
        if down_right:
            if if_reachable(current, down_right):
                g = downright_gn(current)
                if g:
                    if_add_open(current, down_right, g)

        # 5. Check the validation of under point
        down = if_out(h-1, w)
        if down:
            if if_reachable(current, down):
                g = down_gn(current)
                if g:
                    if_add_open(current, down, g)

        # 6. Check the validation of bottom left point
        down_left = if_out(h-1, w-1)
        if down_left:
            if if_reachable(current, down_left):
                g = downleft_gn(current)
                if g:
                    if_add_open(current, down_left, g)

        # 7. Check the validation of left point
        left = if_out(h, w-1)
        if left:
            if if_reachable(current, left):
                g = left_gn(current)
                if g:
                    if_add_open(current, left, g)

        # 8. check the validation of top left point
        up_left = if_out(h+1, w-1)
        if up_left:
            if if_reachable(current, up_left):
                g = upleft_gn(current)
                if g:
                    if_add_open(current, up_left, g)
    print("Due to blocks, no path is found. Please change the map and try again")
    return 0


def retrace_path(node):
    def find_parent(node):
        while node:
            yield node
            node = node.parent
    # Store the coordinates only
    path = [ele.coord for ele in find_parent(node)]
    path.reverse()
    return path
    # path = []
    # while current.parent:
    #     path.append(current)
    #     current = current.parent
    # path.append(current)
    # return path[::-1]
