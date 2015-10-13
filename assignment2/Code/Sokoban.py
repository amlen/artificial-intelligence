__author__ = 'Cyril de Vogelaere : 2814-11-00 & Thuin florian : '

import time
import sys
from copy import deepcopy
from os import listdir, system
from search import *

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

# Read input file and return a state containing the data
def readStateFromGoal(goal):

    grid = readGridFromFile(goal)
    listOfGoalPos = [] #Orginal position of boxes
    j = 0
    for line in grid:
        for i in range(0, len(line)):
            if line[i] == ".":
                #Avatar
                listOfGoalPos.append((i, j))
        j+=1
    return listOfGoalPos

# Read input file and return a state containing the data
def readStateFromInit(init):
    with open(init, "r") as file:
        # Lecture du fichier
        grid = readGridFromFile(init)
        # Creation d'un tableau équivalent au probleme
        avatarPos = (0,0) #Original position of the avatar
        listOfBoxesPos = [] #Orginal position of boxes
        #Read grid for important elem
        j = 0
        for line in grid:
            for i in range(0, len(line)):
                if line[i] == "@":
                    #Avatar
                    avatarPos = (i, j)
                elif line[i] == "$":
                    #Box
                    listOfBoxesPos.append((i, j))
            j+=1
    return State(grid, listOfBoxesPos, avatarPos)

#Add a line of wall
def addALineOfWall(string, length):
    for i in range (0, length+2):
        string += "#"
    string += "\n"
    return string

#################
#   My classes  #
#################

class Sokoban(Problem):
    def __init__(self, init):
        # Extract state from file
        initState = readStateFromInit(init + ".init")
        gridGoal = readStateFromGoal(init + ".goal")
        #Debug print
        print(initState)
        print(gridGoal)
        # Extend super init
        super().__init__(initState)

    def goal_test(self, state):
        pass

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
node = depth_first_tree_search(problem)
# Print
path = node.path()
path.reverse()
for n in path:
    print(n.state)  # assuming that the __str__ function of states output the correct format

#Calculate time elapsed
later = time.time()
print(later - now)
'''