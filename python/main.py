from node import *
import maze as mz
import score
import interface
import time

import numpy as np
import pandas
import time
import sys
import os  

def main():
    maze = mz.Maze("data/small_maze.csv")
    point = score.Scoreboard("data/UID.csv", "team_NTUEE")
    interf = interface.interface()
    # TODO : Initialize necessary variables
    Node_position = 0

    if (sys.argv[1] == '0'):
        print("Mode 0: for treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
        
    elif (sys.argv[1] == '1'):
        print("Mode 1: Self-testing mode.")

        while (Node_position < 6):
            # TODO: You can write your code to test specific function.
            
            #Part 1: read message
            rv = interf.get_message()
            if (rv == ""):          pass
            elif (rv == "Node"):    Node_position = Node_position + 1
            else:                   point.add_UID(rv)

            #Part 2: send cmd
            if (Node_position == 3):
                interf.send_action("L")
        
        interf.end_process()

if __name__ == '__main__':
    main()
