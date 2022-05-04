from audioop import reverse
from cgi import test
from lib2to3.refactor import get_all_fix_names
from pickle import TRUE
from re import A, L
from tracemalloc import start
from node import *
import numpy as np
import csv
import pandas
from enum import IntEnum
import math
import queue
import time

class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    '''
    We can initialize a map as follow:
    __init__(self, filepath, *, STRAIGHT, TURN, REVERSE, starting_point, time_constraint):
        filepath : input a .csv map file
        STRAIGHT : the time taken to go straight per distance unit (default : 0.5)
        TURN : the time taken to turn left/right per time (default : 0.3)
        REVERSE : the time to reverse per time (default : 0.8)
        starting_point : starting point index (default : 1)
        time_constraint : time constraint on the map (default : 90)
    
    If we want to test the correctness of the program, we can use the following method:
    RunAllMaze(self, *, print_order = False, print_time_cost = False, print_action = False, print_score = False, print_detail = False):
        If you only need to get the answer, you just use .all_maze_test() to get the answer.
        If you need to check what the problem is, there are five modes to check our tests:
            print_order : print the order of the passing deadends
            print_time_cost : print the total time cost (with time constraint but still go through all the deadends)
            print_action : print the all action the car should made (type : string)
            print_score : print the total score gotten
            print_detail : print the detail information on the path (including the distance between the two points, ...)
        
    this function will return a string which represents the total action the car should made.
    '''
    def __init__(self, filepath, *, STRAIGHT = 0.5, TURN = 0.3, REVERSE = 0.8, starting_point = 1, time_constraint = 90):
        # TODO : read file and implement a data structure you like
		# For example, when parsing raw_data, you may create several Node objects.  
		# Then you can store these objects into self.nodes.  
		# Finally, add to nd_dictionary by {key(index): value(corresponding node)}

        self.raw_data = pandas.read_csv(filepath)    # pandas.read_csv(_filename_) is a table (frame)
        self.num = len(self.raw_data.index)          # count the number of nodes
        
        # Add nodes to the list "self.nodes"
        self.nodes = []

        # A dictionary with the key be the index of the node and the value be the corresponding "Node" object
        # For example, self.nd_dict[1] represents the node of index 1
        self.nd_dict = dict()

        # Collect all the deadend, set its score and the distance from one endpoint to other endpoints
        self.DeadEnds = []
        self.DeadEndsValue = {}
        self.DeadEndDist = {}

        self.start = starting_point
        self.STRAIGHT = STRAIGHT
        self.TURN = TURN
        self.REVERSE = REVERSE

        self.time_constraint = time_constraint

        #--------------------------------------------------------------------------------
        # read all files
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

            if _node.successor_num == 1:
                self.DeadEnds.append(_index)
        
        # self.nd_dict part
        for _node in self.nodes:
            self.nd_dict[_node.getIndex()] = _node 

    # return starting node (default : 1), it will return a Node object
    def getStartPoint(self):
        if (len(self.nd_dict) < 2):
            print("Error: the start point is not included.")
            return 0
        return self.nd_dict[self.start]
    
    def getStartDirection(self):
        start = self.getStartPoint()
        if start != 0:
            return start.AnyValidDirection()

    def getNodeDict(self):
        return self.nd_dict

    # the same as what we have implemented in the Node class
    def get_two_point_Direction(self, nd_from, nd_to):
        return self.nd_dict[nd_from].getDirection(nd_to)
    
    def getDeadEnds(self):
        return self.DeadEnds

    def __BFS_two_points(self, nd_from, nd_to = 0, mode = 1): 
        if (nd_from == nd_to):
            print("NoNeedToBFSError")
            return 0
        # mode 1 : find the shortest path from nd_from to nd_to
        # mode 2 : find the shortest distance from nd_from to all points
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path

        # define the constant (parameters needed to be tested and revised)
        STRAIGHT = self.STRAIGHT   # the time taken to go straight line per length unit
        TURN = self.TURN       # the time taken to turn left or turn right per time

        # dist[i] = a dict {the adj_node : the shortest distance from nd_from passing the adj_node to i}
        # record the shortest distance between the path from nd_from to any point from each of its adjacent point
        INFTY = 1e5
        dist = {}
        dir = {}
        for i in self.nd_dict.keys():
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
            dir[adj_idx][from_dir] = 0                                      # no need to specify, so the special case to deal with, see Line 192/193
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
                    if last_point == nd_from:       # special case see the BFS_two_point initialization
                        route.append(nd_from)
                        break
                    last_dir = dir[nd_to][neighbor[Node.ADJ_DIR]][1]
                    shortest = dist[nd_to][neighbor[Node.ADJ_DIR]]  # this line avoid being ignored

            # print(last_point, last_dir)

            while last_point != nd_from:   
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
            for i in self.nd_dict.keys():
                _short = INFTY
                for _dir in dist[i].keys():
                    _short = min(dist[i][_dir], _short)
                shortest_dist[i] = _short
                        
            return shortest_dist
        
        else :
            print("ModeError")
            return None

        # you need to run BFS_two_points function when using this, so try to use this function at most one time
    def __getScore(self, endpoint):
        path = self.__BFS_two_points(self.getStartPoint().getIndex(), endpoint)
        north_south_dist = 0
        west_east_dist = 0
        for i in range (0, len(path) - 1):
            now_dir = self.get_two_point_Direction(path[i], path[i + 1]) 
            now_dist = self.nd_dict[path[i]].getDistance(path[i + 1])
            
            if now_dir == Direction.NORTH:
                north_south_dist += now_dist
            elif now_dir == Direction.SOUTH:
                north_south_dist -= now_dist
            elif now_dir == Direction.WEST:
                west_east_dist -= now_dist
            elif now_dir == Direction.EAST:
                west_east_dist += now_dist
            else :
                print("GetScore_DirectionError")

        return abs(north_south_dist) + abs(west_east_dist)

    def __setAllScore(self):
        if self.DeadEndsValue == {}:  # is empty, saving time
            start = self.getStartPoint().getIndex()
            for deadend in self.DeadEnds:
                if deadend != start:
                    self.DeadEndsValue[deadend] = self.__getScore(deadend)
                else:
                    self.DeadEndsValue[deadend] = 0

        return self.DeadEndsValue 

    def __setDeadEndsDistance(self):
        if self.DeadEndDist == {}: # if empty
            for dead in self.DeadEnds:
                _dist_dict = {}
                # return the shortest distance from "dead" to all points
                # note that if dead == 1 then nd_to must not be 1 (NoNeedToBFSError) so we let it be 2
                all_dist = self.__BFS_two_points(dead, nd_to = 1 if dead != 1 else 2, mode = 2) 
                for another_dead in self.DeadEnds:
                    if another_dead != dead:
                        _dist_dict[another_dead] = all_dist[another_dead]
                self.DeadEndDist[dead] = _dist_dict
        
        return self.DeadEndDist  

    # run all the map
    def __Run(self):
        if self.DeadEnds[0] != self.getStartPoint().getIndex():
            print ("StartingPointError")
            return 0

        self.__setAllScore()
        self.__setDeadEndsDistance()

        shortest_path = []
        INFTY = 1e5
        shortest_dist = INFTY   # shortest given the value
        max_score = 0
        time_constraint = self.time_constraint
        REV = self.REVERSE

        def permutation(now, end, total_dist, _path, _score, no_time = False):
            nonlocal shortest_path
            nonlocal shortest_dist
            nonlocal time_constraint
            nonlocal max_score
            if now == end:
                # we first consider the best score case, if we have the same score, we choose the total_dist is the least one
                if (_score > max_score) or (_score == max_score and total_dist < shortest_dist):
                    shortest_dist = total_dist
                    shortest_path = _path[:]   # THIS LINE deep copy!!!
                    max_score = _score
                pass
            else:
                for i in range(now, end):
                    _path[now], _path[i] = _path[i], _path[now]  # swap the position
                    total_dist += self.DeadEndDist[_path[now - 1]][_path[now]]

                    if now > 1:
                        total_dist += REV 

                    # if we have no time, we set no_time = True, not no_time for better efficiency (?)
                    if (not no_time) and total_dist > time_constraint:
                        no_time = True

                    # if we still have time, add score to _score
                    if not no_time:      
                        _score += self.DeadEndsValue[_path[now]]
                    
                    # three conditions to enter the next permutation (recursion), properly cut for better efficiency
                    # condition 1 : if we still have time
                    # condition 2 : if we have better score
                    # condition 3 : if we have the same score but we have shortest_dist in the total map
                    if (not no_time) or _score > max_score or (_score == max_score and total_dist <= shortest_dist):
                        permutation(now + 1, end, total_dist, _path, _score, no_time)
                    
                    if now > 1:
                        total_dist -= REV

                    # if we still have time, remember to substract score to _score
                    if not no_time:
                        _score -= self.DeadEndsValue[_path[now]]         

                    total_dist -= self.DeadEndDist[_path[now - 1]][_path[now]]
                    _path[now], _path[i] = _path[i], _path[now]  # swap back to the original position
                pass

        permutation(1, len(self.DeadEnds), 0, self.DeadEnds, 0, no_time = False)

        return [shortest_path, shortest_dist, max_score]

    def __getAction(self, car_dir, nd_from, nd_to):
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


    # function for tests
    # will print the path of all passing nodes
    # will also print the action the car made 
    def MazeTest(self, nd_from, nd_to):
        
        path = self.__BFS_two_points(nd_from, nd_to)
        print("path:", path)

        # initialize
        now_dir = self.nd_dict[nd_from].AnyValidDirection()
        # now_dir = init_dir

        action_dict = {Action.ADVANCE : "f", Action.U_TURN : "b", Action.TURN_LEFT : "l", Action.TURN_RIGHT : "r"}
        action = []
        answer_string = '' # for website testing
        for i in range (0, len(path) - 1):
            _act = self.__getAction(now_dir, path[i], path[i + 1])
            now_dir = self.get_two_point_Direction(path[i], path[i + 1]) 
            action.append(action_dict[_act])
            answer_string += action_dict[_act] 
    
        print(action)
        print(answer_string)
        pass
    
    def GetTwoPointDistance(self, nd_from, nd_to):
        list = self.__BFS_two_points(nd_from, 0, mode = 2)
        return list[nd_to]

    # almost the same as maze_test, will be used in all_maze_test
    def __action_two_points(self, init_dir, nd_from, nd_to, *, first_step_is_back = False):
        path = self.__BFS_two_points(nd_from, nd_to)
        now_dir = init_dir

        action_dict = {Action.ADVANCE : "f", Action.U_TURN : "b", Action.TURN_LEFT : "l", Action.TURN_RIGHT : "r"}
        answer_string = '' # for website testing
        for i in range (0, len(path) - 1):
            if first_step_is_back and i == 0:
                answer_string += 'b'
            elif (not first_step_is_back) and i == 0:  # to delete the first 'f'
                continue
            else:
                _act = self.__getAction(now_dir, path[i], path[i + 1])
                now_dir = self.get_two_point_Direction(path[i], path[i + 1]) 
                answer_string += action_dict[_act] 

        return answer_string

    def RunAllMaze(self, *, print_order = False, print_time_cost = False, print_action = False, print_score = False, print_detail = False):
        run_result = self.__Run()
        total_path = run_result[0]
        total_cost = run_result[1] 
        total_score = run_result[2]
        total_action = ''
        now_direction = self.getStartDirection()
        
        for i in range(0, len(total_path) - 1):
            _two_points_ans_string = self.__action_two_points(now_direction, total_path[i], total_path[i + 1],\
                                                            first_step_is_back = True if i != 0 else 0)
            now_direction = self.nd_dict[total_path[i + 1]].AnyValidDirection()

            total_action += _two_points_ans_string     

        # three mode for testing
        if print_order:
            print("Deadend order", total_path)
        if print_time_cost:
            print("Total time cost", total_cost)
        if print_action: 
            print("Total_action", total_action)
        if print_score:
            print("Total Score", total_score)
        if print_detail:
            for i in range(0, len(total_path) - 1):
                last = total_path[i]
                now = total_path[i + 1]
                print("The distance between {} and {} is {}".format(last, now, self.get_two_point_distance(last, now)))
                print("The score of tne node {} is {}".format(now, self.DeadEndsValue[now]))

        return total_action

# for test
if __name__ == '__main__':

    # help(Maze)

    begin = time.time()
    # medium_maze.csv is in the file
    #_maze = Maze('medium_maze.csv', STRAIGHT = 0.5, TURN = 0.3, REVERSE = 0.8, starting_point = 1, time_constraint = 90)  
    #_maze = Maze('Test1.csv', time_constraint = 100)
    _maze = Maze('maze_8x6_3.csv', STRAIGHT = 0.62, TURN = 0.4, REVERSE = 0.89)
    #_maze = Maze('Self_test1.csv')

    # print(_maze.maze_test(1, 52))
    # print(_maze.get_two_point_distance(1, 12))
    print(_maze.RunAllMaze(print_score = True))
    
    end = time.time()
    print(end - begin)

    