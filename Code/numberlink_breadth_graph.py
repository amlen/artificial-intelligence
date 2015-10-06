'''NAMES OF THE AUTHOR(S):
    Florian Thuin
    Ivan Ahad'''
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
            self.initial += self.seekLetter(self.grid, self.lettersTab)
            #print("initial" + repr(self.initial))
            #print("initial grid = " +repr(self.grid))
            #start = [0, 0]
            #end = [0, 4]
            #print(pathExists(self.grid, start, end))
            #print("Finish INIT")

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
        # Verification que l'état est viable :
        #print("action =" +repr(action))
        pos = self.lettersTab[action[2]]
        # Si on revient sur un chemin qui était fini :
        if action[2] in self.pathsAlreadyDone:
            #print("Retour sur le chemin de " + action[2])
            del self.pathsAlreadyDone[action[2]]
        # Si on vient de finir un chemin, on l'enregistre et on choisit une
        # nouvelle lettre
        nextToFinish = isNextTo(grid, [action[0], action[1]], pos[2:4], action[2])
        if action[2] not in self.pathsAlreadyDone and nextToFinish:
            #print("4th check")
            self.pathsAlreadyDone[action[2]]=True
            action=self.seekLetter(grid, self.lettersTab).split(",")
        for d in directions:
            stateOK = False
            #print("action in for = " + repr(action))
            i = int(action[0]) + d[0]
            j = int(action[1]) + d[1]
            next = [j, i]
            #print("Next : " + repr(next))
            newgrid = []
            if inBounds(grid, next) and grid[j][i]=="." and not self.isSurround(grid, action[2], [i,j]):
                #print("1st check")
                stateOK = True
                newgrid = list(grid)
                line = newgrid[j]
                newline = line[:i] + action[2] + line[i+1:]
                newgrid[j] = newline
                for letter, pos in self.lettersTab.items():
                    #print("5th check")
                    if letter not in self.pathsAlreadyDone:
                        if letter==action[2] and pathExists(newgrid, [j, i], [pos[3], pos[2]]):
                            #print("Etat OK - if for letter : " + letter)
                            stateOK = True
                        elif pathExists(newgrid, [pos[1], pos[0]] , [pos[3], pos[2]]):
                            #print("2nd check for letter : " + letter + " pos : " + repr(pos))
                            stateOK = True
                        else:
                            #print("3rd check for letter : " + letter + " pos : " + repr(pos))
                            stateOK = False
                            break
                    else:
                        pass
                        #print("la lettre "+ letter + "est dans pathsAlreadyDone wtf")
            if stateOK:
                newstate = self.gridToState(newgrid) + repr(i)+","+repr(j)+","+action[2]
                #print("newstate = " + newstate)
                yield (repr(i) + "," + repr(j) + "," + action[2], newstate)

    def isSurround(self, grid, letter, pos):
        #print("isSurround")
        nLettersAround = 0
        for d in directions:
            i = int(pos[0]) + d[0]
            j = int(pos[1]) + d[1]
            next = [j, i]
            if inBounds(grid, next) and grid[j][i]==letter:
                nLettersAround += 1
        if nLettersAround >= 2:
            if isNextTo(grid, pos, self.lettersTab[letter][2:4],letter) and nLettersAround < 3:
                #print("isSurround return False")
                return False
            else:
                #print("isSurround return True")
                return True
        else:
            #print("isSurround return False 2")
            return False
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

    def seekLetter(self, grid, lettersTab):
        #print("SeekLetter")
        result = ""
        for letter, pos in lettersTab.items():
            nLettersAround = 0
            for d in directions:
                i = d[0] + pos[2]
                j = d[1] + pos[3]
                next = [j, i]
                if inBounds(grid, next) and grid[j][i]==letter:
                    nLettersAround += 1
                    break
            if nLettersAround > 0:
                pass
                #print("La fin de "+ letter+ " est bien connectée")
            else:
                result = result = repr(lettersTab[letter][0]) + "," + repr(lettersTab[letter][1]) + "," + letter
                break
        return result

######################
# Auxiliary function #
######################

directions = [ [-1, 0], [1, 0], [0, -1], [0, 1] ]
square = [ [-1,-1], [-1,1], [1,1], [1,-1] ]

# Cette fonction retourne True si le carré autour de pos (9x9) ne
# contient pas plus de 2 fois la letter, false sinon

def isNextTo(grid, pos, end, letter):
    #print("isNextTo")
    result = False
    for d in directions:
        i = int(pos[0])+d[0]
        j = int(pos[1])+d[1]
        next = [j, i]
        if inBounds(grid, next) and i==end[0] and j==end[1] :
            result=True
            break
    #print("isNextTo return : " +repr(result))
    return result

def pathExists(grid, start, end):
    visited = [ [0 for j in range(0, len(grid[0]))] for i in range(0, len(grid)) ]
    ok = pathExistsDFS(grid, start, end, visited)
    return ok

def pathExistsDFS(grid, start, end, visited):
    #print("Starting at " + repr(start))
    for d in directions:
        i = int(start[0]) + d[0]
        j = int(start[1]) + d[1]
        next = [i, j]
        if i == end[0] and j == end[1]:
            return True
        if inBounds(grid, next) and grid[i][j] == "." and not visited[i][j]:
            #print("Visiting... "+letter+" (" + repr(i) + ","+ repr(j) +")")
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
#example of bfs search
node=breadth_first_graph_search(problem)
#example of print
path=node.path()
path.reverse()
for n in path:
    problem.printState(n.state) #assuming that the __str__ function of states output the correct format
