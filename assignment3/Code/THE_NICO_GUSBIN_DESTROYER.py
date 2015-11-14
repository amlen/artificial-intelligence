from cgitb import enable

__author__ = 'Cyril'
#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2015, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>

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

import avalamImproved
import minimaxImproved
from math import log

################
# My Variables #
################

#On board (ligne, collumn)
#TOPLEFT UP TOPRIGHT LEFT RIGHT DOWNLEFT DOWN DOWNRIGHT
directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

##############
# My Methods #
##############

def getIntegerSign(int):
    if(int > 0):
        return 1
    elif (int < 0):
        return -1
    return 0

def calculate_maxMinMaxDepth(steps, time_left):
    if(time_left == None):
        return 2
    if time_left < 150 and steps > 20:
        return 3
    if time_left < 150:
        return 2
    if time_left < 300 and steps > 25:
        return 4
    if time_left < 300:
        return 3
    if steps > 30:
        return 50
    if steps > 24:
        return 5
    if steps > 14:
        return 4
    if steps > 7:
        return 3
    return 2

#Pre the two tower are adjacent
def couldTowerXJumpOverTowerY(X, Y):
    if X == 0 or Y == 0 or (abs(X) + abs(Y)) > 5:
        return False
    return True

#Pre not a max height tower or an empty pos
def towerScoreEnd(player, board, posX, posY):
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
    if ennemyList.__len__() == 0:
        if(allyList.__len__() == 0):
            return color*2 # 100 % Isolated, fully gained point
    return color #Point for a having more tower than the opponent

#Reduce the number of one of the opponent
def towerScoreStart(player, board, posX, posY):
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
    if ennemyList.__len__() == 0:
        if(allyList.__len__() == 0):
            return color*5 # 100 % Isolated, fully gained point
    if abs(tower) == 1:
        return color*2 #Two points for ones
    return color #Point for a having more tower than the opponent

#Make it very good to have isolated tower of small value !
def calculate_score_end_game(player, board):
    score = 0.0
    #Score for possession of undisputable tower
    for i in range(board.rows):
        for j in range(board.columns):
            #Empty position don't count in the score
            if board.m[i][j] == 0:
                pass
            #Score for possession of undisputable max level tower
            elif abs(board.m[i][j]) == board.max_height:
                score += getIntegerSign(board.m[i][j])*3 # 5 stage tower
            #Calculate score of a tower depending on it's neighbor
            else:
                score += towerScoreEnd(player, board, i, j)
    return score

def calculate_score_start_game(player, board):
    score = 0.0
    #Score for possession of undisputable tower
    for i in range(board.rows):
        for j in range(board.columns):
            #Empty position don't count in the score
            if board.m[i][j] == 0:
                pass
            #Score for possession of undisputable max level tower
            elif abs(board.m[i][j]) == board.max_height:
                score += getIntegerSign(board.m[i][j])*5 # 5 stage tower
            #Calculate score of a tower depending on it's neighbor
            else:
                score += towerScoreStart(player, board, i, j)
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
        if depth >= self.maxMinMaxDepth or oldBoard.is_finished():
            return True
        else:
            return False


    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        (board, player, step) = state
        return calculate_score_start_game(player, board)

    def play(self, board, player, step, time_left):
        """This function is used to play a move according
        to the board, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """

        self.maxMinMaxDepth = calculate_maxMinMaxDepth(step, time_left)
        print("Depth :", self.maxMinMaxDepth)
        print("Time left : ", time_left)
        newBoard = avalamImproved.Board(board.get_percepts(player==avalamImproved.PLAYER2))
        state = (newBoard, player, step)
        return minimaxImproved.search(state, self)


if __name__ == "__main__":
    avalamImproved.agent_main(Agent())
