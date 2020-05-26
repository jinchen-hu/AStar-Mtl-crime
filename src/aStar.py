import numpy as np


class AStar(object):
    def __init__(self, org, des):
        self.__org = np.array(org)
        self.__des = np.array(des)
        self.__close = set()
        self.__open = set()
        self.__path = np.array([[]])

    def fn(self, prt_node, child_point):
        if(prt_node[0]-child_point[0]) != 0 and (prt_node[1] - child_point[1]) != 0:
            g = 1.5
        else:
            g = 1
        return g + prt_node[3]