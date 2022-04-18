from audioop import reverse
from cgi import test
from lib2to3.refactor import get_all_fix_names
from pickle import TRUE
from re import A, L
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


    def BFS_two_points(self, nd_from, nd_to = 1, mode = 1): 
        # mode 1 : find the shortest path from nd_from to nd_to
        # mode 2 : find the shortest distance from nd_from to all points
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path

        # define the constant (parameters needed to be tested and revised)
        STRAIGHT = 0.5   # the time taken to go straight line per length unit
        TURN = 0.3       # the time taken to turn left or turn right per time

        # dist[i] = a dict {the adj_node : the shortest distance from nd_from passing the adj_node to i}
        # record the shortest distance between the path from nd_from to any point from each of its adjacent point
        INFTY = 1e5
        dist = {}
        dir = {}
        for i in range(1, self.num + 1):
            _dist = {}
            _dir = {}
            for neighbor in self.nd_dict[i].getSuccessors():
                # We split all nodes into at most four subnodes to represent the path coming from every direction
                # for example, [3][Direction.NORTH] represents "The north part of the node 3"
                # only the north of the node 3 can have a path to enter [3][Direction.NORTH]
                # assume the west of the node 3 is node 4, there is a path from [3][Direction.NORTH] to [4][Direction.EAST]
                #        4.NORTH                   3.NORTH
                # 4.WEST         4.EAST     3.WEST         3.EAST
                #        4.SOUTH                   3.SOUTH
                _dist[neighbor[Node.ADJ_DIR]] = INFTY      
                _dir[neighbor[Node.ADJ_DIR]] = [0, 0]   # [Adjacent node][Adjacent node.direction]
            dist[i] = _dist
            dir[i] = _dir

        # Begin to BFS, q_bfs means the queue for BFS
        # q_bfs storing the index
        q_bfs = queue.Queue()      

        reverse_dir = {Direction.NORTH : Direction.SOUTH, Direction.SOUTH : Direction.NORTH,\
                        Direction.EAST : Direction.WEST, Direction.WEST : Direction.EAST}

        # initialize and deal with the starting point case
        for neighbor in self.nd_dict[nd_from].getSuccessors():
            dist[nd_from][neighbor[Node.ADJ_DIR]] = 0  # neighbor[Node.ADJ_DIR] means the neighbor's direction

            adj_idx = neighbor[Node.ADJ_INDEX]                              # return the neighbor's index
            from_dir = reverse_dir[neighbor[Node.ADJ_DIR]]                  # the coming direction of adj_idx from nd_from
            dist[adj_idx][from_dir] = neighbor[Node.ADJ_DIST] * STRAIGHT
            dir[adj_idx][from_dir] = 0                                      # no need to specify
            q_bfs.put(adj_idx)    # put all adjacent point into the queue

        while True:
            if q_bfs.empty(): 
                print("QueueEmptyError")
                break
             
            curr_idx = q_bfs.get()               # return the current node index
            curr_node = self.nd_dict[curr_idx]   # return the current node object (type: Node)

            '''
            print("curr_idx", curr_idx)
            print("curr_node", curr_node)
            '''

            for neighbor in curr_node.getSuccessors():
                adj_idx = int(neighbor[Node.ADJ_INDEX])
                adj_dir = neighbor[Node.ADJ_DIR]
                adj_len = neighbor[Node.ADJ_DIST]

                '''
                print("adj_idx", adj_idx)
                print("adj_dir", adj_dir)
                print("adj_len", adj_len)
                '''
                
                put_into_queue = False

                for _neighbor in curr_node.getSuccessors():
                    last_dir = _neighbor[Node.ADJ_DIR]    # the coming direction (_neighbor 3 ---> curr_idx 4) it is Direction.WEST 
                    last_from_dir = reverse_dir[last_dir] # the path direction (_neighbor 3 ---> curr_idx 4) it is Direction.EAST
                    tmp_dist = dist[curr_idx][last_dir] + STRAIGHT * adj_len
                    # consider the turning cost
                    if adj_dir != last_from_dir and curr_idx != nd_from: # actually curr_idx != nd_from can be deleted
                        tmp_dist += TURN

                    # (_neighbor 3 ---> curr_idx 4 ---> adj_idx 5), for 5 we focus dist[5][Direction.WEST]
                    curr_from_dir = reverse_dir[adj_dir]
                    if tmp_dist < dist[adj_idx][curr_from_dir]: # never put equal sign here to prevent infinite loop
                        put_into_queue = True
                        dist[adj_idx][curr_from_dir] = tmp_dist
                        dir[adj_idx][curr_from_dir] = [curr_idx, last_dir]


                if put_into_queue:
                    q_bfs.put(adj_idx)

            if (q_bfs.empty()):
                break
        
        '''
        for i in range(1, self.num + 1):
            for neighbor_dir in dist[i].keys():
                print(i, neighbor_dir, dist[i][neighbor_dir])
        '''

        if mode == 1:  # mode 1 : find the shortest path from nd_from to nd_to
            route = [nd_to]
            passing_node = self.nd_dict[nd_to] # it is a Node object

            # for the endpoint, we find which direction has the shortest path
            shortest = INFTY
            last_point = 0
            last_dir = 0
            for neighbor in passing_node.getSuccessors():
                if dist[nd_to][neighbor[Node.ADJ_DIR]] < shortest:
                    last_point = neighbor[Node.ADJ_INDEX]
                    last_dir = dir[nd_to][neighbor[Node.ADJ_DIR]][1]
                    shortest = dist[nd_to][neighbor[Node.ADJ_DIR]]  # this line avoid being ignored

            # print(last_point, last_dir)

            while True:   
                route.append(int(last_point))
                tmp_point = self.nd_dict[last_point].getSuccessorWithDirection(last_dir)
                # print(last_point, last_dir, tmp_point)
                if tmp_point == nd_from:        # this line to prevent CE
                    route.append(nd_from)
                    break
                last_dir = dir[last_point][last_dir][1]
                last_point = tmp_point

            route.reverse()
            # print(route)
            return route

        elif mode == 2:  # mode 2 : find the shortest distance from nd_from to all points
            shortest_dist = {}
            for i in range(1, self.num + 1):
                _short = INFTY
                for _dir in dist[i].keys():
                    _short = min(dist[i][_dir], _short)
                shortest_dist[i] = _short
                        
            return shortest_dist
        
        else :
            print("ModeError")
            return None
    
    def BFS(self, nd):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        return None

    def getAction(self, car_dir, nd_from, nd_to):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the nd_to is the Successor of nd_to
		# If not, print error message and return 0
        next_dir = self.nd_dict[nd_from].getDirection(nd_to)

        '''
        print("Next Direction", next_dir)
        '''
        
        act = Action
        if next_dir == car_dir:
            act = Action.ADVANCE
        elif next_dir + car_dir == 3 or next_dir + car_dir == 7:
            act = Action.U_TURN
        elif (car_dir == Direction.NORTH and next_dir == Direction.WEST) or (car_dir == Direction.SOUTH and next_dir == Direction.EAST):
            act = Action.TURN_LEFT
        elif (car_dir == Direction.WEST and next_dir == Direction.SOUTH) or (car_dir == Direction.EAST and next_dir == Direction.NORTH):
            act = Action.TURN_LEFT
        elif (car_dir == Direction.NORTH and next_dir == Direction.EAST) or (car_dir == Direction.SOUTH and next_dir == Direction.WEST):
            act = Action.TURN_RIGHT
        elif (car_dir == Direction.WEST and next_dir == Direction.NORTH) or (car_dir == Direction.EAST and next_dir == Direction.SOUTH):
            act = Action.TURN_RIGHT
        else:
            act = Action.HALT
            print("CarActionError")

        return act

    # the same as what we have implemented in the Node class
    def get_two_point_Diection(self, nd_from, nd_to):
        return self.nd_dict[nd_from].getDirection(nd_to)

    def strategy(self, nd):
        return self.BFS(nd)

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)

    # function for tests
    # will print the path of all passing nodes
    # will also print the action the car made 
    def maze_test(self, init_dir, nd_to, nd_from):
        
        path = self.BFS_two_points(nd_to, nd_from)
        print("path:", path)

        now_dir = init_dir

        action_dict = {Action.ADVANCE : "f", Action.U_TURN : "b", Action.TURN_LEFT : "l", Action.TURN_RIGHT : "r"}
        action = []
        answer_string = '' # for website testing
        for i in range (0, len(path) - 1):
            _act = self.getAction(now_dir, path[i], path[i + 1])
            now_dir = self.get_two_point_Diection(path[i], path[i + 1]) 
            action.append(action_dict[_act])
            answer_string += action_dict[_act] 
    
        print(action)
        print(answer_string)
        pass

# for test
if __name__ == '__main__':

    # medium_maze.csv is in the file
    #_maze = Maze('medium_maze.csv')  
    _maze = Maze('Test1.csv')
    #_maze = Maze('Test2.csv')
    #_maze = Maze('Self_test1.csv')

    print(_maze.BFS_two_points(1, 53, mode = 2))
    # print(_maze.getAction(Direction.NORTH, 10, 11))
    #_maze.maze_test(Direction.EAST, 9, 7)
    #_maze.maze_test(Direction.WEST, 1, 53)
    #_maze.maze_test(Direction.WEST, 1, 52)
    #_maze.maze_test(Direction.WEST, 1, 6)
