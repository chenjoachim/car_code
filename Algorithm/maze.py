from re import L
from node import *
import numpy as np
import csv
import pandas
from enum import IntEnum
import math
import queue

class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath):
        # TODO : read file and implement a data structure you like
		# For example, when parsing raw_data, you may create several Node objects.  
		# Then you can store these objects into self.nodes.  
		# Finally, add to nd_dictionary by {key(index): value(corresponding node)}

        self.raw_data = pandas.read_csv(filepath)    # pandas.read_csv(_filename_) is a table (frame)
        self.num = len(self.raw_data.index)          # count the number of nodes
        
        # Add nodes to the list "self.nodes"
        self.nodes = []

        direction = {'North':['ND', Direction.NORTH], 'South':['SD', Direction.SOUTH],\
                    'West':['WD', Direction.WEST], 'East':['ED', Direction.EAST]}
        
        for i in range(0, self.num):
            _index = self.raw_data['index'][i]   # obtain the index of a node
            _node = Node(_index)

            for dir in direction.keys():           # dir = 'North', 'South', 'West', 'East'
                _succ = self.raw_data[dir][i]      # obtain the successor of each direction
                if not np.isnan(_succ):
                    _dist = self.raw_data[direction[dir][0]][i]           # obtain the distance of each direction
                    _node.setSuccessor(_succ, direction[dir][1], _dist)   # set successor (dir_enum[dir] is a Direction object)
    
            self.nodes.append(_node)
        
        # A dictionary with the key be the index of the node and the value be the corresponding "Node" object
        # For example, self.nd_dict[1] represents the node of index 1
        self.nd_dict = dict()
        for _node in self.nodes:
            self.nd_dict[_node.getIndex()] = _node 

    # return the node of index 1 (starting point)
    def getStartPoint(self):
        if (len(self.nd_dict) < 2):
            print("Error: the start point is not included.")
            return 0
        return self.nd_dict[1]

    def getNodeDict(self):
        return self.nd_dict

    def BFS(self, nd):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        return None

    def BFS_two_points(self, nd_from, nd_to):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path

        # define the constant (parameters needed to be tested and revised)
        STRAIGHT = 1.0   # the time taken to go straight line per length unit
        TURN = 0.0       # the time taken to turn left or turn right per time
        REVRESE = 0.0    # the time taken to reverse once

        visit = [False for i in range (0, self.num)]  # an array determine whether a point is visited
        visit[nd_from] = True

        # Begin to BFS, q_bfs means the queue for BFS
        # q_bfs storing three-termed tuple, (current_point, the time has been taken, the direction of the last point to this point)
        q_bfs = queue.Queue()      
        q_bfs.put((nd_from, 0, 0))  

        while True:
            if q_bfs.empty(): 
                print("QueueEmptyError")
                break
            
            



        
        return None

    def getAction(self, car_dir, nd_from, nd_to):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the nd_to is the Successor of nd_to
		# If not, print error message and return 0
        return None

    def strategy(self, nd):
        return self.BFS(nd)

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)

# for test
if __name__ == '__main__':

    # medium_maze.csv is in the file
    test_maze = Maze('medium_maze.csv')  
   