#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2015, <<<<<<<<<<< Gusbin Quentin & Vrielynck Nicolas >>>>>>>>>>>

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

import avalam11
import minimaxAdm
import sys
from random import shuffle

class Agent:
    """This is the agent to play the Avalam game."""

    def __init__(self, name="Agent"):
        self.name = name
        self.map = dict()
        self.hit = 0
        self.nohit = 0
        self.lmt = 3

    def successors(self, state):
        """The successors function must return (or yield) a list of
        pairs (a, s) in which a is the action played to reach the
        state s; s is the new state, i.e. a triplet (b, p, st) where
        b is the new board after the action a has been played,
        p is the player to play the next move and st is the next
        step number.
        """
        (b,p,st) = state
        #si c'est le successor racine, alors on les tries pour améliorer le pruning et faire la "meilleur" décision 
        #en cas d'égalité sur les noeuds.

        if (self.step == st):
            #on met les actions valides dans la listes et on associe un score a chaque action
            action_sort = list()
            for action in b.get_tri_actions(p*self.player):
                if isValid(b,action,p*self.player):
                    c = b.clone()
                    newBoard = c.play_action(action)
                    newScore = newBoard.get_score()
                    action_sort.append((((action,(newBoard,p*-1,st+1))),newScore))
            #si il n'y as pas d'action valide alors on met toutes les actions non valide car il faut retourner qqchose
            if len(action_sort) == 0:
                for action in b.get_tri_actions(p*self.player):
                    c = b.clone()
                    newBoard = c.play_action(action)
                    newScore = newBoard.get_score()
                    action_sort.append((((action,(newBoard,p*-1,st+1))),newScore))

            
            #Dynamic depth si il nous reste assez de temps
            if(self.time_left > 250):
                if (len(action_sort)<165):
                    self.lmt = 4
                if (len(action_sort)<80):
                    self.lmt = 5
                if (len(action_sort)<32):
                    self.lmt = 50
                if (len(action_sort)<35 and self.time_left > 450):
                    self.lmt = 50
            else:
                if(self.step < 20):
                    self.lmt = 3
                else:
                    self.lmt = 4
            
            #Si c'est la limite niveau temps et qu'on a pas assez avance en step alors on diminue la depth pour jouer instant
            if(self.time_left < 100 and self.step < 20):
                self.lmt = 2

            if(self.time_left<20):
                slef.lmt = 2
            

            print("Depth limit = "+str(self.lmt))
            #On tries les actions du plus grand au plus petit
            shuffle(action_sort)
            action_sort.sort(key=lambda tup: tup[1],reverse=True)
            ct = 0
            #on yield les state un par un
            for item in action_sort:
                (action,score) = item
                ct += 1
                #on affiche l'avancement sur la console
                sys.stdout.write("\rAction = " +str(ct)+"/"+str(len(action_sort)))
                sys.stdout.flush()
                if(ct==len(action_sort)):
                    print(" ")
                yield action
              
        #DEPTH 4  
        #si on est en depth 1 et qu'on fait au moins 4 de depth alors on les tries comme a la racine
        elif (self.lmt >3 and self.step == st-1):
            #on met les actions valides dans la listes et on associe un score a chaque action
            action_sort = list()
            for action in b.get_tri_actions(p*self.player):
                if isValid(b,action,p*self.player):
                    c = b.clone()
                    newBoard = c.play_action(action)
                    newScore = newBoard.get_score()
                    action_sort.append((((action,(newBoard,p*-1,st+1))),newScore))
            #si il n'y as pas d'action valide alors on met toutes les actions non valide car il faut retourner qqchose
            if len(action_sort) == 0:
                for action in b.get_tri_actions(p*self.player):
                    c = b.clone()
                    newBoard = c.play_action(action)
                    newScore = newBoard.get_score()
                    action_sort.append((((action,(newBoard,p*-1,st+1))),newScore))

            #On tries les actions du plus petit au plus grand
            action_sort.sort(key=lambda tup: tup[1])

            #on yield les state un par un
            for item in action_sort:
                (action,score) = item
                yield action
         
            
        #DEPTH 5       
        #si on est en depth 2 et qu'on fait au moins 5 de depth alors on les tries comme a la racine
        elif (self.lmt >4 and self.step == st-2):
            #on met les actions valides dans la listes et on associe un score a chaque action
            action_sort = list()
            for action in b.get_tri_actions(p*self.player):
                if isValid(b,action,p*self.player):
                    c = b.clone()
                    newBoard = c.play_action(action)
                    newScore = newBoard.get_score()
                    action_sort.append((((action,(newBoard,p*-1,st+1))),newScore))
            #si il n'y as pas d'action valide alors on met toutes les actions non valide car il faut retourner qqchose
            if len(action_sort) == 0:
                for action in b.get_tri_actions(p*self.player):
                    c = b.clone()
                    newBoard = c.play_action(action)
                    newScore = newBoard.get_score()
                    action_sort.append((((action,(newBoard,p*-1,st+1))),newScore))

            ##On tries les actions du plus grand au plus petit
            action_sort.sort(key=lambda tup: tup[1],reverse=True)

            #on yield les state un par un
            for item in action_sort:
                (action,score) = item
                yield action
            
        
        #sinon on les tries pas, on vérifie juste les moves
        else:
            valid = False
            #On vérifie si il y a des actions valide (move enemi sur sois = pas valide)
            for action in b.get_tri_actions(p*self.player):
                if isValid(b,action,p*self.player):
                    valid = True
                    break

            #Si il y a des actions valides on les faits 
            if(valid):
                for action in b.get_tri_actions(p*self.player):
                    if isValid(b,action,p*self.player):
                        c = b.clone()
                        newBoard = c.play_action(action)
                        yield((action,(newBoard,p*-1,st+1)))
            #sinon on parcours toutes les actions
            else:
                for action in b.get_tri_actions(p*self.player):
                    c = b.clone()
                    newBoard = c.play_action(action)
                    yield((action,(newBoard,p*-1,st+1)))
  
    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        (b,p,st) = state
        #si on a atteind notre limite de depth alors on stop
        if(depth>=self.lmt):
            return True
        #si il n'y as plus d'action a faire sur le board alors on stop
        if b.is_finished():
            return True
        return False

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        (b,p,st) = state
        score = b.get_score()

        return score
                

    def play(self, board, player, step, time_left):
        """This function is used to play a move according
        to the board, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """

        '''
        #Si c'est le premier step on hardcode le move
        if(step==1):
            return (0,2,1,2)
        '''

        self.step = step

        if time_left is not None:
            self.time_left = time_left
        else:
            self.time_left = 300
        print("Temps restant Adm = "+str(time_left))

        #percept
        if(step%2==0):
            self.player = -1
        else:
            self.player = 1
        newBoard = avalam11.Board(board.get_percepts(player==avalam11.PLAYER2))


        state = (newBoard, player, step)
        return minimaxAdm.search(state, self)

if __name__ == "__main__":
    avalam11.agent_main(Agent())

#Return True if the action is valid for the player, return false otherwise
#An action is considered as not valid if we replace one of the player tower by an enemi one
def isValid(board,action,player):
    x1,y1,x2,y2 = action
    #si la tour 1 appartient à l'enemi
    if(board.m[x1][y1]*player < 0):
        #et que la tour 2 nous appartient, alors c'est pas valide
        if(board.m[x2][y2]*player > 0):
            #print("Joueur "+str(player)+" - 1 = "+str(board.m[x1][y1])+" - 2 ="+str(board.m[x2][y2])+" - Non valide")
            return False
    #print("Joueur "+str(player)+" - 1 = "+str(board.m[x1][y1])+" - 2 ="+str(board.m[x2][y2])+" - valide")
    return True

