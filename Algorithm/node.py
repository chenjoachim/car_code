from enum import IntEnum
from numpy import ndarray

# You can get the enumeration based on integer value, or make comparison
# ex: d = Direction(1), then d would be Direction.NORTH
# ex: print(Direction.SOUTH == 1) should return False
class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST  = 3
    EAST  = 4

# Construct class Node and its member functions
# You may add more member functions to meet your needs
class Node:
    def __init__(self, index=0):
        self.index = index
        # store successor as (Node, direction to node, distance)
        self.Successors = []                                                                                             

    def getIndex(self):
        return self.index

    def getSuccessors(self):
        return self.Successors

    def setSuccessor(self, successor, direction, length=1):
        self.Successors.append((successor, Direction(direction), int(length)))
        print("For Node {}, a successor {} is set.".format(self.index, self.Successors[-1]))
        return


    def getDirection(self, nd):
        # TODO : if nd is adjacent to the present node, return the direction of nd from the present node
        # For example, if the direction of nd from the present node is EAST, then return Direction.EAST = 4
		# However, if nd is not adjacent to the present node, print error message and return 0 
        for succ in self.Successors:
            if succ[0] == nd:
                return succ[1]
        
        print("DirectionError")
        return 0

    def isSuccessor(self, nd):
        for succ in self.Successors:
            if succ[0] == nd: 
                return True
        return False

# For test
if __name__ == '__main__':
    nd = Node(1)
    nd.setSuccessor(2, Direction.SOUTH, 3)
    nd.setSuccessor(4, Direction.NORTH)

    print(nd.getDirection(2))
    print(nd.getDirection(4))
    print(nd.getDirection(3))



