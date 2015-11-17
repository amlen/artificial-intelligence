# -*- coding: utf-8 -*-
"""
Common definitions for the Avalam players.
Copyright (C) 2010 - Vianney le Clément, UCLouvain

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

PLAYER1 = 1
PLAYER2 = -1
#TOPLEFT UP TOPRIGHT LEFT RIGHT DOWNLEFT DOWN DOWNRIGHT
directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

#Get the color of a position
def getIntegerSign(int):
    if(int > 0):
        return 1
    elif (int < 0):
        return -1
    return 0

def binnaryInsert(list, action, value, i, j):
    x = (int) ((i+j)/2)
    if x == i or j <= i:
        list.insert(i, (action, value))
        return
    elif list[x][1] < value:
        binnaryInsert(list, action, value, x, j)
    elif list[x][1] > value:
        binnaryInsert(list, action, value, i, x)
    else:
        list.insert(x, (action, value))
        return

def fuseSortList(listOne, listTwo, value):
    for action in listTwo:
        binnaryInsert(listOne, action, value, 0, len(listOne)-1)

def removeReverseActionFromList(list):
    for i in range(0, len(list)):
        (A, B, C, D) = list[i]
        for j in range(i+1, len(list)):
            if (C, D, A, B) == list[j]:
                list.pop(j)
                break
    return list

def removeOverlappingActions(list):
    i = 0
    while i < len(list):
        j = i+1
        (A, B, C, D) = list[i]
        while j < len(list):
            (E, F, G, H) = list[j]
            if (A, B) == (E, F) or (A, B) == (G, H) or (C, D) == (E, F) or (C, D) == (G, H):
                list.pop(j)
            else:
                j += 1
        i += 1
    return list

class InvalidAction(Exception):

    """Raised when an invalid action is played."""

    def __init__(self, action=None):
        self.action = action


class Board:

    """Representation of an Avalam Board.

    self.m is a self.rows by self.columns bi-dimensional array representing the
    board.  The absolute value of a cell is the height of the tower.  The sign
    is the color of the top-most counter (negative for red, positive for
    yellow).

    """

    # standard avalam
    max_height = 5
    initial_board = [ [ 0,  0,  1, -1,  0,  0,  0,  0,  0],
                      [ 0,  1, -1,  1, -1,  0,  0,  0,  0],
                      [ 0, -1,  1, -1,  1, -1,  1,  0,  0],
                      [ 0,  1, -1,  1, -1,  1, -1,  1, -1],
                      [ 1, -1,  1, -1,  0, -1,  1, -1,  1],
                      [-1,  1, -1,  1, -1,  1, -1,  1,  0],
                      [ 0,  0,  1, -1,  1, -1,  1, -1,  0],
                      [ 0,  0,  0,  0, -1,  1, -1,  1,  0],
                      [ 0,  0,  0,  0,  0, -1,  1,  0,  0] ]

    def __init__(self, percepts=initial_board, max_height=max_height,
                       invert=False):
        """Initialize the board.

        Arguments:
        percepts -- matrix representing the board
        invert -- whether to invert the sign of all values, inverting the
            players
        max_height -- maximum height of a tower

        """
        self.m = percepts
        self.rows = len(self.m)
        self.columns = len(self.m[0])
        self.max_height = max_height
        self.m = self.get_percepts(invert)  # make a copy of the percepts

    def __str__(self):
        def str_cell(i, j):
            x = self.m[i][j]
            if x:
                return "%+2d" % x
            else:
                return " ."
        return "\n".join(" ".join(str_cell(i, j) for j in range(self.columns))
                         for i in range(self.rows))

    def clone(self):
        """Return a clone of this object."""
        return Board(self.m)

    def get_percepts(self, invert=False):
        """Return the percepts corresponding to the current state.

        If invert is True, the sign of all values is inverted to get the view
        of the other player.

        """
        mul = 1
        if invert:
            mul = -1
        return [[mul * self.m[i][j] for j in range(self.columns)]
                for i in range(self.rows)]

    def get_towers(self):
        """Yield all towers.

        Yield the towers as triplets (i, j, h):
        i -- row number of the tower
        j -- column number of the tower
        h -- height of the tower (absolute value) and owner (sign)

        """
        for i in range(self.rows):
            for j in range(self.columns):
                if self.m[i][j]:
                    yield (i, j, self.m[i][j])

    def is_action_valid(self, action):
        """Return whether action is a valid action."""
        try:
            i1, j1, i2, j2 = action
            if i1 < 0 or j1 < 0 or i2 < 0 or j2 < 0 or \
               i1 >= self.rows or j1 >= self.columns or \
               i2 >= self.rows or j2 >= self.columns or \
               (i1 == i2 and j1 == j2) or (abs(i1-i2) > 1) or (abs(j1-j2) > 1):
                return False
            h1 = abs(self.m[i1][j1])
            h2 = abs(self.m[i2][j2])
            if h1 <= 0 or h1 >= self.max_height or h2 <= 0 or \
                    h2 >= self.max_height or h1+h2 > self.max_height:
                return False
            return True
        except (TypeError, ValueError):
            return False

    def get_tower_actions(self, i, j):
        """Yield all actions with moving tower (i,j)"""
        h = abs(self.m[i][j])
        if h > 0 and h < self.max_height:
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    action = (i, j, i+di, j+dj)
                    if self.is_action_valid(action):
                        yield action

    def is_tower_movable(self, i, j):
        """Return wether tower (i,j) is movable"""
        for action in self.get_tower_actions(i, j):
            return True
        return False

    def get_actions(self):
        """Yield all valid actions on this board."""
        for i, j, h in self.get_towers():
            for action in self.get_tower_actions(i, j):
                yield action

    def get_sorted_actions(self, player):
        crucialActionList = []
        strongActionList = []
        weak3relatedActionList = []
        weak2relatedActionList = []
        weak1relatedActionList = []
        for i, j, h in self.get_towers():
            elemCounter = 0
            tempStrongActionList = []
            tempWeak3relatedActionList = []
            tempWeak2relatedActionList = []
            tempWeak1relatedActionList = []
            for action in self.get_tower_actions(i, j):
                elemCounter += 1
                currentTower = abs(h)
                adjTower = abs(self.m[action[2]][action[3]])
                if currentTower + adjTower < 5:
                    if max(currentTower, adjTower) == 3:
                        tempWeak3relatedActionList.append(action)
                    elif max(currentTower, adjTower) == 2:
                        tempWeak2relatedActionList.append(action)
                    elif max(currentTower, adjTower) == 1:
                        tempWeak1relatedActionList.append(action)
                elif currentTower + adjTower == 5:
                    tempStrongActionList.append(action)
            if elemCounter == 1:
                #Nearly isolated => crucial move
                crucialActionList.extend(tempStrongActionList)
                crucialActionList.extend(tempWeak3relatedActionList)
                crucialActionList.extend(tempWeak2relatedActionList)
                crucialActionList.extend(tempWeak1relatedActionList)
            else:
                #Normal move
                if getIntegerSign(self.m[i][j]) == player:
                    tempStrongActionList.extend(strongActionList)
                    strongActionList = tempStrongActionList
                else:
                    strongActionList.extend(tempStrongActionList)
                fuseSortList(weak3relatedActionList, tempWeak3relatedActionList, elemCounter)
                fuseSortList(weak2relatedActionList, tempWeak2relatedActionList, elemCounter)
                fuseSortList(weak1relatedActionList, tempWeak1relatedActionList, elemCounter)
        for action in crucialActionList:
            yield action
        for action in strongActionList:
            yield action
        for action in weak3relatedActionList:
            yield action[0]
        for action in weak2relatedActionList:
            yield action[0]
        for action in weak1relatedActionList:
            yield action[0]


    def estimate_depth_safety(self):
        crucialActionList = []
        strongActionList = []
        for i in range(self.rows):
            for j in range(self.columns):
                #Empty position don't count in the score
                currentTower = abs(self.m[i][j])
                if not (currentTower == 0 or currentTower == self.max_height):
                    tempStrongActionList = []
                    tempWeakActionList = []
                    elemCounter = 0
                    for modX, modY in directions:
                        posX = i + modX
                        posY = j + modY
                        if self.inBounds(posX, posY):
                            adjTower = abs(self.m[posX][posY])
                            if not (adjTower == 0 or adjTower == self.max_height):
                                if currentTower + adjTower < 5:
                                    elemCounter += 1
                                    tempWeakActionList.append((i, j, posX, posY))
                                elif currentTower + adjTower == 5:
                                    tempStrongActionList.append((i, j, posX, posY))
                                    elemCounter += 1
                    if elemCounter == 1:
                        #Nearly isolated => crucial move
                        crucialActionList.extend(tempStrongActionList)
                        crucialActionList.extend(tempWeakActionList)
                    else:
                        #Normal move
                        strongActionList.extend(tempStrongActionList)
        crucialActionList.extend(strongActionList)
        #Debug print
        print(crucialActionList)
        res = removeOverlappingActions(crucialActionList)
        #DebugPrint
        print(res)
        #return
        return len(res)

    def play_action(self, action):
        """Play an action if it is valid.

        An action is a 4-uple containing the row and column of the tower to
        move and the row and column of the tower to gobble. If the action is
        invalid, raise an InvalidAction exception. Return self.

        """
        if not self.is_action_valid(action):
            raise InvalidAction(action)
        i1, j1, i2, j2 = action
        h1 = abs(self.m[i1][j1])
        h2 = abs(self.m[i2][j2])
        if self.m[i1][j1] < 0:
            self.m[i2][j2] = -(h1 + h2)
        else:
            self.m[i2][j2] = h1 + h2
        self.m[i1][j1] = 0
        return self

    def is_finished(self):
        """Return whether no more moves can be made (i.e., game finished)."""
        for action in self.get_actions():
            return False
        return True

    def get_score(self):
        """Return a score for this board.

        The score is the difference between the number of towers of each
        player. In case of ties, it is the difference between the maximal
        height towers of each player. If self.is_finished() returns True,
        this score represents the winner (<0: red, >0: yellow, 0: draw).

        """
        score = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.m[i][j] < 0:
                    score -= 1
                elif self.m[i][j] > 0:
                    score += 1
        if score == 0:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.m[i][j] == -self.max_height:
                        score -= 1
                    elif self.m[i][j] == self.max_height:
                        score += 1
        return score
    
    def __str__(self):
        return '' + repr(self.m)

    def inBounds(self, posX, posY):
        return 0 <= posX and posX < len(self.m) and 0 <= posY and posY < len(self.m[0])

def load_percepts(filename):
    """Load percepts from a CSV file."""
    f = None
    try:
        f = open(filename, "r")
        import csv
        percepts = []
        for row in csv.reader(f):
            if not row:
                continue
            row = [int(c.strip()) for c in row]
            if percepts:
                assert len(row) == len(percepts[0]), \
                       "rows must have the same length"
            percepts.append(row)
        return percepts
    finally:
        if f is not None:
            f.close()


class Agent:
  """Interface for a Zombies agent"""

  def initialize(self, percepts, players, time_left):
    """Begin a new game.

    The computation done here also counts in the time credit.

    Arguments:
    percepts -- the initial board in a form that can be fed to the Board
        constructor.
    players -- sequence of players this agent controls
    time_left -- a float giving the number of seconds left from the time
        credit for this agent (all players taken together). If the game is
        not time-limited, time_left is None.

    """
    pass

  def play(self, percepts, player, step, time_left):
    """Play and return an action.

    Arguments:
    percepts -- the current board in a form that can be fed to the Board
        constructor.
    player -- the player to control in this step
    step -- the current step number, starting from 1
    time_left -- a float giving the number of seconds left from the time
        credit. If the game is not time-limited, time_left is None.

    """
    pass

  def agent_main(agent, args_cb=None, setup_cb=None):
    """Launch agent server depending on arguments.

    Arguments:
    agent -- an Agent instance
    args_cb -- function taking two arguments: the agent and an
        ArgumentParser. It can add custom options to the parser.
        (None to disable)
    setup_cb -- function taking three arguments: the agent, the
        ArgumentParser and the options dictionary. It can be used to
        configure the agent based on the custom options. (None to
        disable)
  
    """
    pass
