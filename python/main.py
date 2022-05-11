from node import *
import maze as mz
import score        #for local
import remote       #for remote grading
import interface
import time

import numpy as np
import pandas
import time
import sys
import os  

def main():
    try:
        #TODO: !!!!!!!!!!!!!!!DON'T FORGET TO CHANGE MAZE NAME!!!!!!!!!!!!!!!!!!
        #=================================HERE==================================
        #NORMAL MODE (V = 9.0)
        maze = mz.Maze("data/medium_maze.csv", STRAIGHT = 0.512, TURN = 0.317, REVERSE = 0.687)

        #FAST MODE (V = )
        # maze = mz.Maze("data/maze_8x6_3.csv", )
        #=================================HERE==================================

        route = maze.RunAllMaze(print_score = True)
        interf = interface.interface(route)
        # TODO : Initialize necessary variables
        Node_position = 0

        if (len(sys.argv) < 3 or sys.argv[2] == '0'):  point = remote.Scoreboard("fakepath", "tunococ")
        elif (sys.argv[2] == '1'):    point = score.Scoreboard("data/UID.csv", "team_NTUEE")
        # time.sleep(5)
        # TODO: open before the game
        interf.send_action("start")
        if (len(sys.argv) < 2 or sys.argv[1] == '0'):
            print("Mode 0: for treasure-hunting")
            # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
            while (True):
                rv = interf.get_message()
                if (rv == ""):
                    pass
                else:                   
                    point.add_UID(rv)

        elif (sys.argv[1] == '1'):
            print("Mode 1: Self-testing mode.")
            while (Node_position < 6):
                # TODO: You can write your code to test specific function.
                
                #Part 1: read message
                rv = interf.get_message()
                if (rv == ""):          
                    pass
                elif (rv == "Node"):    
                    Node_position = Node_position + 1
                    print("This is node", Node_position)
                else:                   
                    point.add_UID(rv)
            
            interf.end_process()
    except KeyboardInterrupt:
        interf.end_process()
        print("Program end")
        sys.exit(0)

if __name__ == '__main__':
    main()
