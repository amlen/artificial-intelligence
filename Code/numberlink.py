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
        self.lettersTab = {}
        self.pathsAlreadyDone = {}
        with open(init, "r") as file:
            # Lecture du fichier
            data_read = file.read()
            self.initial = data_read

            # Création d'un tableau équivalent au problème
            self.grid = data_read.split("\n")
            self.grid.pop()
            self.width=len(self.grid[0])
            self.height=len(self.grid)
            j=0
            for line in self.grid:
                for i in range(0, len(line)):
                    if not (line[i]== "." or line[i] in self.lettersTab):
                        self.lettersTab[line[i]]= [i, j, None, None]
                    elif not line[i]==".":
                        self.lettersTab[line[i]][2]=i
                        self.lettersTab[line[i]][3]=j
                j+=1

            #print("Nombre de lettres = " + repr(len(self.lettersTab)))
            #print("Nombre de colonnes = " + repr(self.width))
            #print("Nombre de lignes = " + repr(self.height))

            # Création de la première action (identique
            # au placement d'une lettre sur le tableau)
            self.initial = self.initial.replace("\n", "")
            self.initial += self.seekLetter(self.lettersTab)
            #print("initial" + repr(self.initial))
            #print("initial grid = " +repr(self.grid))
            start = [0, 0]
            end = [0, 4]
            #print(pathExists(self.grid, start, end))

    def goal_test(self, state):
        #self.printState(state)
        state = state[0:self.width*self.height-1]
        if state.count(".") > 0:
                return False
        return True

    def successor(self, state):
        grid = self.stateToGrid(state)
        action = grid.pop().split(",")
        #print("Grid :")
        #self.printState(state)
        #print("Action : \n" + repr(action))
        stateIsViable = True
        # Verification que l'état est viable :
        for letter, pos in self.lettersTab.items():
            #print("Successor on letter : " + letter)
            # Si le path pour la lettre est déjà créé :
            pathIsCreated = pathExists(grid, [pos[1], pos[0]], [pos[3], pos[2]], letter)
            if letter in self.pathsAlreadyDone and not pathIsCreated:
                del self.pathsAlreadyDone[letter]
            if letter not in self.pathsAlreadyDone and pathIsCreated:
                #print("Le path de " + letter + " est fini")
                self.pathsAlreadyDone[letter] = True
            # Si le path pour la lettre peut exister :
            elif pathExists(grid, [pos[1], pos[0]], [pos[3], pos[2]]):
                pass
                #print("Le path pour " + letter + " existe toujours")
            # Si le path est en cours de construction :
            elif letter==action[2] and pathExists(grid, [int(action[1]), int(action[0])], [pos[3],pos[2]]):
                pass
                #print("Le path pour " + letter + " est en cours de construction")
            elif pathIsCreated:
                pass
            else:
                #print("L'état n'est plus viable pour " + letter)
                stateIsViable=False
                break
        if stateIsViable:
            #print("Création d'un state viable")
            letterToAdd = action[2]
            for letter, pos in self.lettersTab.items():
                if letterToAdd in self.pathsAlreadyDone:
                    newaction=self.seekLetter(self.lettersTab).split(",")
                    letterToAdd=newaction[2]
                    action[0]=newaction[0]
                    action[1]=newaction[1]
                else:
                    break
            if letterToAdd not in self.pathsAlreadyDone:
                for d in directions:
                    i = int(action[0]) + d[0]
                    j = int(action[1]) + d[1]
                    next = [j, i]
                    if inBounds(grid, next) and grid[j][i] == "." and not isSurround(grid, letterToAdd, [i, j]):
                        #newgrid est une copie indépendante de grid
                        newgrid = list(grid)
                        line = newgrid[j]
                        newline = line[:i] + letterToAdd + line[i+1:]
                        newgrid[j] = newline
                        #print("Mettre " + letterToAdd + " à (" +
                        #        repr(i) + "," + repr(j) + ")")
                        newstate = self.gridToState(newgrid)
                        yield (repr(i) + "," + repr(j) + "," +
                                letterToAdd, self.gridToState(newgrid) +
                                repr(i) + "," + repr(j) + "," +
                                letterToAdd)
        else:
            return None

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
        #print("STATE in gridToState = " + state)
        for i in range(0, len(state), self.width):
            if i < self.width:
                grid.append(state[0:self.width])
            else:
                grid.append(state[i:i+self.width])
            visitedLines += 1
            if (visitedLines == self.height):
                action = state[i+self.width:]
                break
        #print("ACTION=" + repr(action))
        grid.append(action)
        return grid

    def printState(self, state):
        for i in range(0, self.height):
            print(state[(i*self.width):(i+1)*self.width])
        print("")

    def seekLetter(self, lettersTab):
        keys = list(lettersTab.keys())
        curX = len(keys)*2
        curY = curX
        curLetter = keys[0]
        for letter, pos in lettersTab.items():
            if letter not in self.pathsAlreadyDone:
                x1 = pos[0]
                x2 = pos[2]
                y1 = pos[1]
                y2 = pos[3]
                x = x2-x1
                y = y2-y1
                if curX > x and curY > y:
                    curX = x
                    curY = y
                    curLetter = letter
        return repr(lettersTab[curLetter][0]) +","+ repr(lettersTab[curLetter][1]) +","+ curLetter

######################
# Auxiliary function #
######################

directions = [ [-1, 0], [1, 0], [0, -1], [0, 1] ]
square = [ [-1,-1], [-1,1], [1,1], [1,-1] ]

# Cette fonction retourne True si le carré autour de pos (9x9) ne
# contient pas plus de 2 fois la letter, false sinon
def isSurround(grid, letter, pos):
    nLettersAround = 0
    for d in directions:
        i = int(pos[0]) + d[0]
        j = int(pos[1]) + d[1]
        next = [j, i]
        if inBounds(grid, next) and grid[j][i]==letter:
            nLettersAround += 1
    if nLettersAround > 2:
        return True
    else:
        for d in square:
            i = int(pos[0]) + d[0]
            j = int(pos[1]) + d[1]
            next = [j, i]
            if inBounds(grid, next) and grid[j][i]==letter:
                nLettersAround += 1
                if nLettersAround >= 7:
                    return True
                else:
                    return False

def pathExists(grid, start, end, letter="."):
    visited = [ [0 for j in range(0, len(grid[0]))] for i in range(0, len(grid)) ]
    ok = pathExistsDFS(grid, start, end, visited, letter)
    return ok

def pathExistsDFS(grid, start, end, visited, letter):
    #print("Starting at " + repr(start))
    for d in directions:
        i = start[0] + d[0]
        j = start[1] + d[1]
        next = [i, j]
        if i == end[0] and j == end[1]:
            return True
        if inBounds(grid, next) and grid[i][j] == letter and not visited[i][j]:
            #print("Visiting... "+letter+" (" + repr(i) + ","+ repr(j) +")")
            visited[i][j] = 1
            exists = pathExistsDFS(grid, next, end, visited, letter)
            if exists:
                return True
    return False

def inBounds(grid, pos):
    return 0 <= pos[0] and pos[0] < len(grid) and 0 <= pos[1] and pos[1] < len(grid[0])

#####################
# Launch the search #
#####################

problem=NumberLink(sys.argv[1])
#example of bfs search
node=depth_first_graph_search(problem)
#example of print
path=node.path()
path.reverse()
for n in path:
    problem.printState(n.state) #assuming that the __str__ function of states output the correct format
