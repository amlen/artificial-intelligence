#!/usr/bin/env python3
# coding: utf-8

from cgitb import enable

__author__ = 'Cyril'

"""
Avalam agent.
Copyright (C) 2015, Cyril de Vogelaere, Florian Thuin

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""

import avalam
import minimax
import datetime
import time
import math

################
# My Variables #
################

#On board (ligne, collumn)
#TOPLEFT UP TOPRIGHT LEFT RIGHT DOWNLEFT DOWN DOWNRIGHT
directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
MAX_STEPS = 35
MAX_STEPS_PLAYED = 18
##############
# My Methods #
##############

#Get the color of a position
def getIntegerSign(int):
    if(int > 0):
        return 1
    elif (int < 0):
        return -1
    return 0

def getStepSafeDepth(steps, time_left):
    basePossibilities = 300 - (10*(steps))
    currentNbPossibilties = basePossibilities
    depthEstimated = 1
    while currentNbPossibilties < time_left*1000*steps: #10000000:
        if basePossibilities <= 0 or currentNbPossibilties <= 0 or depthEstimated > 5:
            return 5
        currentNbPossibilties *= (basePossibilities - (10*depthEstimated))
        depthEstimated+=1
    return depthEstimated

def getTimeSituation(steps, time_left, gametime):
    return time_left - (gametime / MAX_STEPS_PLAYED)*(MAX_STEPS_PLAYED - math.ceil(steps/2))

def calculate_maxMinMaxDepth(steps, time_left, gametime, depth_safety):
    #Obvious return
    if(time_left == None or depth_safety > 0):
        return 2
    if(time_left < (MAX_STEPS - steps)*2):
        return 1
    #Calculate safe depth
    safeDepth = getStepSafeDepth(steps, time_left)
    #Evaluate
    timeSituation= getTimeSituation(steps, time_left, gametime)
    if timeSituation > 0:
        #Avance sur le planning
        if safeDepth == 2 and timeSituation > (MAX_STEPS - steps)*5:
            safeDepth += 1
        if safeDepth == 3 and timeSituation > (MAX_STEPS - steps)*10:
            safeDepth += 1
        if safeDepth == 4 and timeSituation > (MAX_STEPS - steps)*15:
            safeDepth += 1
    else:
        #Retard
        return 2
    return safeDepth



#Pre the two tower are adjacent
def couldTowerXJumpOverTowerY(X, Y):
    if X == 0 or Y == 0 or (abs(X) + abs(Y)) > 5:
        return False
    return True

def couldSnapBackWork(board, snapBackTower, tower, posX, posY):
    #Init
    color = getIntegerSign(tower)
    allyList = []
    ennemyList = []
    #Init ally and ennemy List
    for dir in directions:
        testX = posX + dir[0]
        testY = posY + dir[1]
        if board.inBounds(testX, testY) and couldTowerXJumpOverTowerY(board.m[testX][testY], tower):
            if getIntegerSign(board.m[testX][testY]) == color:
                allyList.append((board.m[testX][testY], testX, testY))
            elif getIntegerSign(board.m[testX][testY]) == -color:
                ennemyList.append((board.m[testX][testY], testX, testY))
    #Remove the tower we want to check !
    if getIntegerSign(snapBackTower[0]) == color :
        allyList.remove(snapBackTower)
    else :
        ennemyList.remove(snapBackTower)
    #Check snapback isolating case
    if len(ennemyList) == 0:
        for ally in allyList:
            if couldTowerXJumpOverTowerY(abs(snapBackTower[0]) + abs(tower), ally[0]):
                return True
        return False
    #Check snapback 5 tower case
    for allyTower, _, _ in allyList:
        if(abs(allyTower) + abs(snapBackTower[0]) + abs(tower) == board.max_height):
            return True
    return False

# Evaluate the score of a non level 5 tower
def towerScore(board, posX, posY):
    #Init
    tower = board.m[posX][posY]
    color = getIntegerSign(tower)
    allyList = []
    ennemyList = []
    #Init ally and ennemy List
    for dir in directions:
        testX = posX + dir[0]
        testY = posY + dir[1]
        if board.inBounds(testX, testY) and couldTowerXJumpOverTowerY(board.m[testX][testY], tower):
            if getIntegerSign(board.m[testX][testY]) == color:
                allyList.append((board.m[testX][testY], testX, testY))
            elif getIntegerSign(board.m[testX][testY]) == -color:
                ennemyList.append((board.m[testX][testY], testX, testY))
    #Score for possesion of an undisputable isolated tower
    if ennemyList.__len__() == 0 and allyList.__len__() == 0:
        return color*7 # 100 % Isolated, fully gained point
    #Check for snapback on tower
    if not (abs(tower) == 3 or abs(tower) == 4) or allyList.__len__() == 0 : #Else tower of level three would too easily be in snapback
        snapback = True
        for val, x, y in allyList:
            if not couldSnapBackWork(board, (tower, posX, posY), val, x, y):
                snapback = False
                break
        if snapback:
            for val, x, y in ennemyList:
                if not couldSnapBackWork(board, (tower, posX, posY), val, x, y):
                    snapback = False
                    break
        if snapback:
            return 0 # 1 points for a snapback (other tower in snapback give points too so carefull with that)
    # Nothing weird about these towers, juste give normal points
    if abs(tower) == 1:
        return color*1.5 #Two points for ones, because ones are possibilities
    if abs(tower) == 2:
        return color*1 #1.5 points for twos, because twos are also possibilities
    return color*0.5 #Point for a having more tower than the opponent

# Calculate board score
def calculate_score(board):
    score = 0.0
    for i in range(board.rows):
        for j in range(board.columns):
            #Empty position don't count in the score
            if board.m[i][j] == 0:
                pass
            #Score for possession of undisputable max level tower
            elif abs(board.m[i][j]) == board.max_height:
                score += getIntegerSign(board.m[i][j])*8 # 5 stage tower
            #Calculate score of a tower depending on it's neighbor
            else:
                score += towerScore(board, i, j)
    return score

############
# My Agent #
############

class Agent:
    """This is the skeleton of an agent to play the Avalam game."""

    def __init__(self, name="Basic Agent"):
        self.name = name

    def successors(self, state):
        """The successors function must return (or yield) a list of
        pairs (a, s) in which a is the action played to reach the
        state s; s is the new state, i.e. a triplet (b, p, st) where
        b is the new board after the action a has been played,
        p is the player to play the next move and st is the next
        step number.
        """
        #Return result
        (oldBoard, oldPlayer, oldStepNbr) = state
        for action in oldBoard.get_sorted_actions():
            newBoard = oldBoard.clone()
            newBoard.play_action(action)
            yield (action, (newBoard, -oldPlayer, oldStepNbr+1))

    #Depth depending on time
    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        (oldBoard, oldPlayer, oldStepNbr) = state
        if self.maxMinMaxDepth > 2 and datetime.datetime.now() > self.maxTimeForMinMax:
            if depth >= 2:
                return True
            return False
        if depth >= self.maxMinMaxDepth or oldBoard.is_finished():
            return True
        else:
            return False


    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        (board, player, step) = state
        return calculate_score(board)

    def play(self, board, player, step, time_left):
        """This function is used to play a move according
        to the board, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        #Launch
        if (step == 1 or step == 2):
            self.gametime = time_left
        if (step == 1):
            # Hard codage de la 1ï¿½re action pour ï¿½viter une perte de temps
            return (3, 8, 4, 7)
        #Init minmax
        newBoard = avalam.Board(board.get_percepts(player==avalam.PLAYER2))
        state = (newBoard, player, step)
        self.maxMinMaxDepth = calculate_maxMinMaxDepth(step, time_left, self.gametime, newBoard.estimate_depth_safety())
        self.maxTimeForMinMax = datetime.datetime.now() + datetime.timedelta(0, getTimeSituation(step, time_left, self.gametime))
        #Debug
        print("Depth :", self.maxMinMaxDepth)
        print("Time :", getTimeSituation(step, time_left, self.gametime))
        print("Time left : ", time_left)
        #Minmax
        minmaxRes = minimax.search(state, self, time_left)
        print(minmaxRes)
        if minmaxRes == None:
            self.maxMinMaxDepth = 2
            minmaxRes = minimax.search(state, self, time_left)
        return minmaxRes

if __name__ == "__main__":
    avalam.agent_main(Agent())
