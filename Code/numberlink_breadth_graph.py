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
        self.numberOfNodesVisited = 0
        with open(init, "r") as file:
            # Lecture du fichier
            data_read = file.read()
            self.initial = data_read

            # Création d'un tableau équivalent au problème
            # et de variables globales utiles pour la suite
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

            # Création de la première action (identique
            # au placement d'une lettre sur le tableau)
            self.initial = self.initial.replace("\n", "")
            self.initial += self.seekLetter(self.grid, self.lettersTab)

    def goal_test(self, state):
        self.numberOfNodesVisited += 1
        state = state[0:self.width*self.height-1]
        if state.count(".") > 0:
                return False
        return True

    def successor(self, state):
        grid = self.stateToGrid(state)
        action = grid.pop().split(",")
        pos = self.lettersTab[action[2]]
        if action[2] in self.pathsAlreadyDone:
            del self.pathsAlreadyDone[action[2]]
        # Si on vient de finir un chemin, on l'enregistre et on choisit une
        # nouvelle lettre
        nextToFinish = isNextTo(grid, [action[0], action[1]], pos[2:4], action[2])
        if action[2] not in self.pathsAlreadyDone and nextToFinish:
            self.pathsAlreadyDone[action[2]]=True
            action=self.seekLetter(grid, self.lettersTab).split(",")
        for d in directions:
            stateOK = False
            i = int(action[0]) + d[0]
            j = int(action[1]) + d[1]
            next = [j, i]
            newgrid = []
            # Vérification que le futur cas est viable
            if inBounds(grid, next) and grid[j][i]=="." and not self.isSurround(grid, action[2], [i,j]):
                stateOK = True
                newgrid = list(grid)
                line = newgrid[j]
                newline = line[:i] + action[2] + line[i+1:]
                newgrid[j] = newline
                for letter, pos in self.lettersTab.items():
                    if self.letterWasFinished(grid, [pos[2], pos[3]], letter):
                        self.pathsAlreadyDone[letter] = True
                    if letter not in self.pathsAlreadyDone:
                        if letter==action[2] and pathExists(newgrid, [j, i], [pos[3], pos[2]]):
                            stateOK = True
                        elif pathExists(newgrid, [pos[1], pos[0]] , [pos[3], pos[2]]):
                            stateOK = True
                        else:
                            stateOK = False
                            break
                    else:
                        pass
            # Si le cas est viable, on le retourne sous la forme (action, state)
            if stateOK:
                newstate = self.gridToState(newgrid) + repr(i)+","+repr(j)+","+action[2]
                yield (repr(i) + "," + repr(j) + "," + action[2], newstate)

    def letterWasFinished(self, grid, pos, letter):
    	# Vérifie que la fin d'une lettre est reliée ou non à un path
        result = False
        for d in directions:
            i = pos[0]+d[0]
            j = pos[1]+d[1]
            next = [j, i]
            if inBounds(grid, next) and grid[j][i]==letter:
                result = True
                break
        return result

    def isSurround(self, grid, letter, pos):
    	# Permet de vérifier que deux lettres ne sont pas présentes autour d'une position
    	# sur un grid. 
        nLettersAround = 0
        for d in directions:
            i = int(pos[0]) + d[0]
            j = int(pos[1]) + d[1]
            next = [j, i]
            if inBounds(grid, next) and grid[j][i]==letter:
                nLettersAround += 1
        if nLettersAround >= 2:
            if isNextTo(grid, pos, self.lettersTab[letter][2:4],letter) and nLettersAround < 3:
                return False
            else:
                return True
        else:
            return False
    def gridToState(self, grid):
    	# Transforme un grid (tableau) en state (string)
        state = ""
        for line in grid:
            state += line
        return state

    def stateToGrid(self, state):
        # Creation du grid (tableau) à partir d'un state (string)
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
                action = state[i+self.width:]
                break
        grid.append(action)
        return grid

    def printState(self, state):
    	# Imprime un state (string) sous forme de tableau
        for i in range(0, self.height):
            print(state[(i*self.width):(i+1)*self.width])
        print("")

    def seekLetter(self, grid, lettersTab):
    	# Recherche une lettre qui n'a pas encore été terminée
        result = ""
        for letter, pos in sorted(lettersTab.items()):
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
print("Nombre de noeuds solution : " + repr(len(path)))
print("Nombre de noeuds visités : " + repr(problem.numberOfNodesVisited))
for n in path:
    problem.printState(n.state) #assuming that the __str__ function of states output the correct format
