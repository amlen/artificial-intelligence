__author__ = 'Cyril de Vogelaere : 2814-11-00 & Thuin florian : 0656-11-00'

import time
import sys
from copy import deepcopy
from os import listdir, system
from search import *

# LEFT RIGHT UP DOWN
directions = [[0, -1], [0, 1], [-1, 0], [1, 0]]
global listOfGoalPos

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
        # Creation d'un tableau equivalent au probleme
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
    if box in listOfGoalPos :
        # If box on goal state, it's never a KO state
        return False
    #Test LEFT AND RIGHT
    freedom = 0
    for x in range(0, 2):
        i = box[0] + directions[x][0]
        j = box[1] + directions[x][1]
        if inBounds(state.grid, (i, j)) and (state.grid[i][j] == " " or state.grid[i][j] == "@"):
            freedom += 1;
    if freedom == 2:
        return False
    #Test LEFT AND RIGHT
    freedom = 0
    for x in range(2, 4):
        i = box[0] + directions[x][0]
        j = box[1] + directions[x][1]
        if inBounds(state.grid, (i, j)) and (state.grid[i][j] == " " or state.grid[i][j] == "@"):
            freedom += 1;
    if freedom == 2:
        return False
    return False

# Check if pushing box will lead to a KO state
def isPushingOK(state, dir, x, y):
    result = False
    state.grid[x] = state.grid[x][:y] + " " + state.grid[x][y+1:]
    newBoxX = x + dir[0]
    newBoxY = y + dir[1]
    state.grid[newBoxX] = state.grid[newBoxX][:newBoxY] + "$" + state.grid[newBoxX][newBoxY+1:]
    result = not isKOState(state, (newBoxX, newBoxY))
    state.grid[newBoxX] = state.grid[newBoxX][:newBoxY] + " " + state.grid[newBoxX][newBoxY+1:]
    state.grid[x] = state.grid[x][:y] + "$" + state.grid[x][y+1:]
    return result

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

#Generate successor from state
#Pre : Successor can be generated
def generateSuccessor(state, dir):
    newState = deepcopy(state)
    #Calculate new avatar pos
    newState.avatarPos = (state.avatarPos[0] + dir[0], state.avatarPos[1] + dir[1])
    #Clear old pos in grid, update avatar pos in state
    newState.grid[state.avatarPos[0]] = newState.grid[state.avatarPos[0]][:state.avatarPos[1]] + " " + newState.grid[state.avatarPos[0]][state.avatarPos[1]+1:]
    if(newState.grid[newState.avatarPos[0]][newState.avatarPos[1]] == "$"):
        #Move box before updating avatar in grid
        for index in range(0, len(newState.listOfBoxesPos)):
            if (newState.avatarPos[0], newState.avatarPos[1]) == newState.listOfBoxesPos[index]:
                #Calculate new coordinate
                newX = dir[0] + newState.avatarPos[0]
                newY = dir[1] + newState.avatarPos[1]
                newState.listOfBoxesPos[index] = (newX, newY)
                newState.grid[newX] = newState.grid[newX][:newY] + "$" + newState.grid[newX][newY+1:]
    #Update avatar in grid
    newState.grid[newState.avatarPos[0]] = newState.grid[newState.avatarPos[0]][:newState.avatarPos[1]] + "@" + newState.grid[newState.avatarPos[0]][newState.avatarPos[1]+1:]
    return newState


# Return the minimum hamilton distance to reach a goal
def minDistOfBoxToGoal(state, box):
    best = len(state.grid) + len(state.grid[0])
    for goal in listOfGoalPos:
        best = min(best, (abs(goal[0] - box[0]) + abs(goal[1] - box[1])))
    return best

# Heuristic function
# Minimal value will be explored first !!!
def heuristicFunction(node):
    score = 0
    for box in node.state.listOfBoxesPos:
        #if box not in listOfGoalPos:
        #    score += 50 # Solve everything but 04
        #score += minDistOfBoxToGoal(node.state, box) * 50 #Fails 04 and 15
        #score += minDistOfBoxToGoal(node.state, box) * len(node.state.grid) * len(node.state.grid[0]) #Fails 04 and 15
        score += minDistOfBoxToGoal(node.state, box) * len(node.state.grid) # Passes everything
    return score


#################
#   My classes  #
#################

class Sokoban(Problem):
    def __init__(self, init):
        # Extract state from file
        global listOfGoalPos
        listOfGoalPos = readStateFromGoal(init + ".goal")
        initState = readStateFromInit(init + ".init")
        # Extend super init
        super().__init__(initState)

    def goal_test(self, state):
        for elem in listOfGoalPos:
            if not elem in state.listOfBoxesPos:
                return False
        return True

    def successor(self, state):
        #print(state)
        for i in range(0, len(directions)):
            x = state.avatarPos[0] + directions[i][0]
            y = state.avatarPos[1] + directions[i][1]
            if inBounds(state.grid, (x, y)) and (state.grid[x][y] == ' ' or (state.grid[x][y] == '$' and canPushBox(state.grid, state.avatarPos, (x,y)) and isPushingOK(state, directions[i], x, y))):
                #Yield result
                yield (i, generateSuccessor(state, directions[i]))


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

# Solve using bfs search
#node = depth_first_graph_search(problem)
node = astar_graph_search(problem, heuristicFunction)
# Print
path = node.path()
path.reverse()
for n in path:
    print(n.state)  # assuming that the __str__ function of states output the correct format

#Calculate time elapsed
later = time.time()
print(later - now)