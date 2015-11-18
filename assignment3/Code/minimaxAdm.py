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


def search(state, game, prune=True):
    """Perform a MiniMax/AlphaBeta search and return the best action.

    Arguments:
    state -- initial state
    game -- a concrete instance of class Game
    prune -- whether to use AlphaBeta pruning

    """
    #If the value is already in the map then we return the value else we calcule it and store it in the map
    def getOrElseUpdate(state,game,depth):
        (b,p,st) = state
        string = ''.join(str(e) for e in b.m)
        dictionnary = game.map
        if string in dictionnary:
            game.hit = game.hit +1          
            return dictionnary[string]
        else:
            game.nohit = game.nohit +1
            val = game.evaluate(state)
            dictionnary[string] = val
            return val
        

    def max_value(state, alpha, beta, depth,game):
        (b,p,st) = state
        if game.cutoff(state, depth):
            return getOrElseUpdate(state,game,depth), None
        val = -inf
        action = None
        for a, s in game.successors(state):
            v, _ = min_value(s, alpha, beta, depth + 1,game)
            if v > val:
                val = v
                action = a
                if prune:
                    if v >= beta:
                        return v, a
                    alpha = max(alpha, v)
        return val, action

    def min_value(state, alpha, beta, depth,game):
        (b,p,st) = state
        if game.cutoff(state, depth):
            return getOrElseUpdate(state,game,depth), None
        val = inf
        action = None
        for a, s in game.successors(state):
            v, _ = max_value(s, alpha, beta, depth + 1,game)
            if v < val:
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        return v, a
                    beta = min(beta, v)
        return val, action
    _, action = max_value(state, -inf, inf,0,game)
    #Affichage des hit et no hit sur notre map
    #print("Hit "+ str(game.hit))
    #print("NoHit "+ str(game.nohit))
    game.map.clear()
    (b,p,st) = state
    #print("Score Actuel = "+str(b.get_score()))
    c = b.clone()
    c.play_action(action)
    #print("Score Now = "+str(c.get_score()))
    return action