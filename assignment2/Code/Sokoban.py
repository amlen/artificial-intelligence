__author__ = 'Cyril de Vogelaere : 2814-11-00 & Thuin florian : '

import time
import sys
from copy import deepcopy
from os import listdir, system
from search import *


# LEFT RIGHT UP DOWN
directions = [[0, -1], [0, 1], [-1, 0], [1, 0]]

###############
# My function #
###############

def readGridFromFile(Texte):
    with open(Texte, "r") as file:
        data_read = file.read()
        grid = data_read.split("\n")
        #Remove empty line
        grid.pop()
        #Remove last line
        grid.pop()
        #Remove first line
        grid.pop(0)
        #Truncate first and last collumn
        for i in range(0, len(grid)):
            grid[i] = grid[i][1 : len(grid[i])-1]
        return grid

# Read goal file and return a grid containing the data
def readStateFromGoal(goal):

    grid = readGridFromFile(goal)
    listOfGoalPos = [] #Orginal position of boxes
    i = 0
    for line in grid:
        for j in range(0, len(line)):
            if line[j] == ".":
                #Avatar
                listOfGoalPos.append((i, j))
        i+=1
    return listOfGoalPos

# Read init file and return a state containing the data
def readStateFromInit(init):
    with open(init, "r") as file:
        # Lecture du fichier
        grid = readGridFromFile(init)
        # Creation d'un tableau équivalent au probleme
        avatarPos = (0,0) #Original position of the avatar
        listOfBoxesPos = [] #Orginal position of boxes
        #Read grid for important elem
        i = 0
        for line in grid:
            for j in range(0, len(line)):
                if line[j] == "@":
                    #Avatar
                    avatarPos = (i, j)
                elif line[j] == "$":
                    #Box
                    listOfBoxesPos.append((i, j))
            i+=1
    return State(grid, listOfBoxesPos, avatarPos)

#Add a line of wall
def addALineOfWall(string, length):
    for i in range (0, length+2):
        string += "#"
    string += "\n"
    return string

#Check if position is inbound
def inBounds(grid, pos):
    return 0 <= pos[0] and pos[0] < len(grid) and 0 <= pos[1] and pos[1] < len(grid[0])

#Check if the state is a KO state
def isKOState(state, box):
    #Check direction in which i can push
    if box in state.listOfGoalPos :
        # If box on goal state, it's never a KO state
        return False
    freedom = 0
    for d in directions:
        i = box[0] + d[0]
        j = box[1] + d[1]
        if inBounds(state.grid, (i, j)) and state.grid[i][j] == " ":
            freedom += 1;
    return freedom < 3

#Check if two position are adjacent
def arePosAdjacent(posA, posB):
    distI = abs(posA[0] - posB[0])
    distJ = abs(posA[1] - posB[1])
    return (distI + distJ) < 2

#Check if char can push the box from this position
def canPushBox(grid, char, box):
    if arePosAdjacent(char, box):
        i = 2*box[0] - char[0]
        j = 2*box[1] - char[1]
        if inBounds(grid, (i, j)) and grid[i][j] == " ":
            return True
    return False


#################
#   My classes  #
#################

class Sokoban(Problem):
    def __init__(self, init):
        # Extract state from file
        self.listOfGoalPos = readStateFromGoal(init + ".goal")
        initState = readStateFromInit(init + ".init")
        #Debug print
        print(initState)
        print(initState.__repr__())
        # Extend super init
        super().__init__(initState)

    def goal_test(self, state):
        for elem in self.listOfGoalPos:
            if not elem in state.listOfBoxesPos :
                return False
        return True

    def successor(self, state):
        pass

class State:
    def __init__(self, gridInit, listOfBoxesPos, avatarPos):
        # Save state variable
        self.listOfBoxesPos = listOfBoxesPos
        self.avatarPos = avatarPos
        self.grid = gridInit

    def __str__(self):  # Jolie representation
        string = ""
        string = addALineOfWall(string, len(self.grid[0]))
        for a in range(0, len(self.grid)):
            string += "#"
            for b in range(0, len(self.grid[a])):
                string += self.grid[a][b]
            string += "#"
            string += "\n"
        string = addALineOfWall(string, len(self.grid[0]))
        return string

    def __repr__(self):  # Full representation
        return str((self.avatarPos, self.listOfBoxesPos, self.grid))

    def __eq__(self, other):
        return (other.grid == self.grid)

    def __hash__(self):
        return self.__str__().__hash__()

#####################
# Launch the search #
#####################

# Init
now = time.time()
problem = Sokoban(sys.argv[1])

'''
# Solve using bfs search
node = astar_graph_search(problem, TODO FUNCTION H)
# Print
path = node.path()
path.reverse()
for n in path:
    print(n.state)  # assuming that the __str__ function of states output the correct format

#Calculate time elapsed
later = time.time()
print(later - now)
'''