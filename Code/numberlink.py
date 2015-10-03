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
            data_read = file.read()
            self.initial = data_read
            self.grid = data_read.split("\n")
            self.grid.pop()
            self.width=len(self.grid[0])
            self.height=len(self.grid)
            print("Nombre de colonnes = " + repr(self.width))
            print("Nombre de lignes = " + repr(self.height))
            self.initial += "0,0,A"
            print(repr(self.grid))
            start = [0, 0]
            end = [0, 4]
            print(pathExists(self.grid, start, end))

    def goal_test(self, state):
        state.pop()
        for lines in state:
            if lines.count(".") > 0:
                return False
        return True

    def successor(self, state):
        newstate = state
        action = newstate.pop().split(",")
        if (action[0] == "None"):
            action=seekLetter(newstate).split(",")
        for d in directions:
            i = int(action[0]) + d[0]
            j = int(action[1]) + d[1]
            if i>=0 and j>=0 and i < self.width and j < self.height:
                line = newstate[i]
                newline = line[:j] + action[2] + line[j+1:]
                newstate[i] = newline
                newstate.append(repr(i) +","+ repr(j) +","+repr(action[2]))
                yield newstate

######################
# Auxiliary function #
######################

directions = [ [-1, 0], [1, 0], [0, -1], [0, 1] ]

def gridToState(grid):
    state = ""
    for line in grid:
        state += line
    return state

def stateToGrid(state):
    # Creation du grid
    grid = []
    visitedLines = 0
    state = state.replace("\n", "")
    action = object()
    for i in range(0, len(state), self.width):
        if i < self.width:
            grid.append(state[0:self.width])
        else:
            grid.append(state[i:i+self.width])
        visitedLines += 1
        if (visitedLines == self.height):
            action = state[i+self.width:].split(",")
            break
    grid += action
    return grid
def seekLetter(state):
    j = 0
    for line in state:
        for i in range(0 , len(line)):
            if not line[i]=='.':
                return repr(j) + ","+ repr(i) + ","+state[i][j]
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
print(problem.stateToGrid(problem.initial))
#example of bfs search
###node=depth_first_graph_search(problem)
#example of print
###path=node.path()
###path.reverse()
###for n in path:
###    print(n.state) #assuming that the __str__ function of states output the correct format
