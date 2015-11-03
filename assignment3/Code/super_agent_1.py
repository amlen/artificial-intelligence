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

import avalam
import minimax
import utils

################
# My Variables #
################

#On board (ligne, collumn)
#TOPLEFT UP TOPRIGHT LEFT RIGHT DOWNLEFT DOWN DOWNRIGHT
directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

##############
# My Methods #
##############

def inBounds(board, pos):
    return 0 <= pos[0] and pos[0] < len(board.m) and 0 <= pos[1] and pos[1] < len(board.m[0])

def getIntegerSign(int):
    if(int > 0):
        return 1
    return -1

def calculate_maxMinMaxDepth(steps, time_left):
    if(time_left < 50):
        return 2
    else:
        return (int)(2 + (steps/15))

#Pre the two tower are adjacent
def couldTowerXJumpOverTowerY(X, Y):
    #Drop if same sign or if can't jump on each other due to value too big
    if X == 0 or Y == 0 or (abs(X) + abs(Y)) > 5:
        return False
    return True

def isIsolated(board, posX, posY):
    #Calculate remaining value for tower
    tower = board.m[posX][posY]
    #See if the tower is isolated
    for dir in directions:
        testX = posX + dir[0]
        testY = posY + dir[1]
        if inBounds(board, (testX, testY)) and couldTowerXJumpOverTowerY(board.m[testX][testY], tower):
            return False
    return True

def calculate_accurate_score(board, player):
    score = 0
    #Score based on pure number of stones
    #Score for possession of undisputable tower
    for i in range(board.rows):
        for j in range(board.columns):
            #Empty position don't count in the score
            if board.m[i][j] == 0:
                pass
            #Score for possession of undisputable max level tower
            elif board.m[i][j] == -board.max_height or board.m[i][j] == board.max_height:
                score += getIntegerSign(board.m[i][j])*15 # 15 points only for max level tower so merging two isolated tower is not considered a better move
            #score for giving the possibility of having undisputable tower
            #Score for possesion of an undisputable isolated tower
            elif isIsolated(board, i, j):
                score += getIntegerSign(board.m[i][j])*10 # 10 point for each isolated tower
            #Basic score for having more tower than the opponnent
            else:
                score += getIntegerSign(board.m[i][j])
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
        for action in oldBoard.get_actions():
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
        (oldBoard, oldPlayer, oldStepNbr) = state
        return calculate_accurate_score(oldBoard, oldPlayer)

    def play(self, board, player, step, time_left):
        """This function is used to play a move according
        to the board, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        self.time_left = time_left
        self.maxMinMaxDepth = calculate_maxMinMaxDepth(step, time_left)
        newBoard = avalam.Board(board.get_percepts(player==avalam.PLAYER2))
        state = (newBoard, player, step)
        return minimax.search(state, self)


if __name__ == "__main__":
    avalam.agent_main(Agent())
