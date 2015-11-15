"""
MiniMax and AlphaBeta algorithms.
Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
Copyright (C) 2014, Université catholique de Louvain

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
import sys
import random

global steps

class Game:

    """Abstract base class for a game."""

    def successors(self, state):
        """Return the successors of state as (action, state) pairs."""
        abstract

    def cutoff(self, state, depth):
        """Return whether state should be expanded further.

        This function should at least check whether state is a finishing
        state and return True in that case.

        """
        abstract

    def evaluate(self, state):
        """Return the evaluation of state."""
        abstract


inf = float("inf")

def insertInLexicalOrder(actionList, action):
    (A, B, C, D) = action
    newStr = str(A) + " " + str(B) + " " + str(C) + " " + str(D)
    i = 0
    while i in range(0, len(actionList)):
        if(newStr < actionList[i]):
            break
        i+=1
    actionList.insert(i, newStr)
    return i

def getStringFromActionList(actionList):
    res = ""
    for action in actionList:
        res += action + " "
    res.rstrip()
    return res

#Doesn't evaluate two times the same state
def search(state, game, time_left, prune=True):
    """Perform a MiniMax/AlphaBeta search and return the best action.

    Arguments:
    state -- initial state
    game -- a concrete instance of class Game
    prune -- whether to use AlphaBeta pruning

    """
    dictionnary = {}

    def max_value(state, alpha, beta, depth, actionList):
        if game.cutoff(state, depth):
            # Return score
            key = getStringFromActionList(actionList)
            if key not in dictionnary:
                score = game.evaluate(state)
                dictionnary[key] = score
                return score, None
            return dictionnary[key], None
        val = -inf
        action = None
        for a, s in game.successors(state):
            if depth == 0:
                global steps
                steps += 1
                sys.stdout.write("\rAction child of root : {0} >> ".format(steps))
                sys.stdout.flush()
            popIndex = insertInLexicalOrder(actionList, a)
            v, _ = min_value(s, alpha, beta, depth + 1, actionList)
            actionList.pop(popIndex)
            if v == val and random.randint(0, 1000) == 0:
                action = action
            elif v > val:
                val = v
                action = a
                if prune:
                    if v >= beta:
                        return v, a
                    alpha = max(alpha, v)
        return val, action

    def min_value(state, alpha, beta, depth, actionList):
        if game.cutoff(state, depth):
            # Return score
            key = getStringFromActionList(actionList)
            if key not in dictionnary:
                score = game.evaluate(state)
                dictionnary[key] = score
                return score, None
            return dictionnary[key], None
        val = inf
        action = None
        for a, s in game.successors(state):
            popIndex = insertInLexicalOrder(actionList, a)
            v, _ = max_value(s, alpha, beta, depth + 1, actionList)
            actionList.pop(popIndex)
            if v == val and random.randint(0, 1000) == 0:
                action = action
            elif v < val:
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        return v, a
                    beta = min(beta, v)
        return val, action

    global steps
    steps = 0
    _, action = max_value(state, -inf, inf, 0, [])
    return action