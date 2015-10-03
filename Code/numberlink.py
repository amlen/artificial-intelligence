'''NAMES OF THE AUTHOR(S): TODO'''
import time
import sys
from os import listdir,system
from search import *

#################
# Problem class #
#################

class NumberLink(Problem):

    def __init__(self, init):
        self.width =  0
        self.height = 0
        with open(init, "r") as file:
            # Lecture du fichier
            data_read = file.read()
            self.initial = data_read

            # Création d'un tableau équivalent au problème
            self.grid = data_read.split("\n")
            self.grid.pop()
            self.width=len(self.grid[0])
            self.height=len(self.grid)
            print("Nombre de colonnes = " + repr(self.width))
            print("Nombre de lignes = " + repr(self.height))

            # Création de la première action (identique
            # au placement d'une lettre sur le tableau)
            self.initial += seekLetter(self.initial)
            print("initial" + repr(self.initial))
            print("initial grid = " +repr(self.grid))
            start = [0, 0]
            end = [0, 4]
            print(pathExists(self.grid, start, end))

    def goal_test(self, state):
        state = state[0:self.width*self.height-1]
        if state.count(".") > 0:
                return False
        return True

    def successor(self, state):
        grid = self.stateToGrid(state)
        action = grid.pop().split(",")
        print("OLD ACTION =" + repr(action))
        for d in directions:
            i = int(action[0]) + d[0]
            j = int(action[1]) + d[1]
            if i>=0 and j>=0 and i < self.width and j < self.height and grid[j][i]=='.':
                print("YIELDING : " + action[2] + " in (" + repr(i) + "," +
                      repr(j) + ")")
                line = grid[j]
                newline = line[:i] + action[2] + line[i+1:]
                grid[j] = newline
                yield (repr(i) + "," + repr(j) + "," + action[2], self.gridToState(grid))

    def gridToState(self, grid):
        state = ""
        for line in grid:
            state += line
        return state

    def stateToGrid(self, state):
        # Creation du grid
        grid = []
        visitedLines = 0
        state = state.replace("\n", "")
        action = object()
        print("STATE in gridToState = " + state)
        for i in range(0, len(state), self.width):
            if i < self.width:
                grid.append(state[0:self.width])
            else:
                grid.append(state[i:i+self.width])
            visitedLines += 1
            if (visitedLines == self.height):
                action = state[i+self.width:]
                break
        print("ACTION=" + repr(action))
        grid.append(action)
        return grid

    def printState(self, state):
        for i in range(0, self.height):
            print(state[(i*self.width):(i+1)*self.width])



######################
# Auxiliary function #
######################

directions = [ [-1, 0], [1, 0], [0, -1], [0, 1] ]

def seekLetter(state):
    j = 0
    for line in state:
        for i in range(0 , len(line)):
            if not line[i]=='.':
                return repr(j) + "," + repr(i) + "," + state[i][j]
        j += 1

def pathExists(grid, start, end):
    visited = [ [0 for j in range(0, len(grid[0]))] for i in range(0, len(grid)) ]
    ok = pathExistsDFS(grid, start, end, visited)
    return ok

def pathExistsDFS(grid, start, end, visited):
	for d in directions:
		i = start[0] + d[0]
		j = start[1] + d[1]
		next = [i, j]
		if i == end[0] and j == end[1]:
			return True
		if inBounds(grid, next) and grid[i][j] == '.' and not visited[i][j]:
			visited[i][j] = 1
			exists = pathExistsDFS(grid, next, end, visited)
			if exists:
				return True
	return False

def inBounds(grid, pos):
    return 0 <= pos[0] and pos[0] < len(grid) and 0 <= pos[1] and pos[1] < len(grid[0])

#####################
# Launch the search #
#####################



problem=NumberLink(sys.argv[1])
#problem.successor(problem.initial)
for i in problem.successor(problem.initial):
    print("i[1]=" + i[1])
    problem.printState(i[1])
    for j in problem.successor(i[1]+i[0]):
        print("Second nodes")
        problem.printState(j[1])
        for k in problem.successor(j[1]+j[0]):
            print("Third nodes")
            problem.printState(k[1])
#example of bfs search
###node=depth_first_graph_search(problem)
#example of print
###path=node.path()
###path.reverse()
###for n in path:
###    print(n.state) #assuming that the __str__ function of states output the correct format
