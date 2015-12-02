#! /usr/bin/env python3
# coding: utf-8
##########################################################################
#
#		Implementation of the wedding problem class
#
##########################################################################
from search import Problem, LSNode, random_walk
from copy import deepcopy
from random import random, randint, seed, choice
import sys

#################
# Problem class #
#################

def table_value(table, m):
    '''
    table is a list of people
    m is an affinity matrix of the people
    '''
    value = 0
    for e1 in table:
        for e2 in table:
            value += m[e1][e2]
    return value

def switch_people(person1, person2, state):
    '''
    Changes the state by switching person1
    and person2 in the tables they are assigned
    to.
    The tables will be changed, the value of the state will be updated.
    '''
    table1 = None
    ind1 = -1
    table2 = None
    ind2 = -1
    # Récupère les gens dans les tables
    for table in state.tables:
        if table1 == None:
            try:
                ind1 = table.index(person1)
                table1 = table
            except ValueError as _:
                pass
        if table2 == None:
            try:
                ind2 = table.index(person2)
                table2 = table
            except ValueError as _:
                pass
        if table1 != None and table2 != None:
            break

    # Calcule l'ancienne valeur d'affinité
    old_value = 0
    old_value += table_value(table1, state.m)
    old_value += table_value(table2, state.m)
    # switch des gens
    #print(state.tables)
    table1[ind1] = person2
    table2[ind2] = person1
    #print(state.tables)
    # calcul de la nouvelle valeur de l'affinité
    new_value = 0
    new_value += table_value(table1, state.m)
    new_value += table_value(table2, state.m)
    state.value = state.value - old_value + new_value

class Wedding(Problem):
    def __init__(self, init):
        self.swap = {}
        number_participants = 0
        number_tables = 0
        with open(init, 'r') as f:
            # read_data = f.read()
            number_participants = int(f.readline())
            number_tables = int(f.readline())
            number_participants_by_table = int(
                number_participants / number_tables)
            grid = {}
            i = 0
            for line in f:
                grid[i] = [int(i) for i in line.split()]
                i += 1
            assigned_people = {}
            i = 0
            tables = []
            value = 0
            while i < number_participants:
                if i not in assigned_people:
                    assigned_people[i] = True
                    cnt = 1
                    table = [i]
                    line = list(grid[i])
                    while cnt < number_participants_by_table:
                        m = max(line)
                        ind = line.index(m)
                        if ind not in assigned_people:
                            assigned_people[ind] = True
                            table.append(ind)
                            cnt += 1
                        line[ind] = -sys.maxsize
                    value += table_value(table, grid)
                    tables.append(sorted(table))
                i += 1
            Problem.__init__(self, State(
                number_participants, number_tables, grid, list(tables), value))

    def successor(self, state):
        new_state = deepcopy(state)
        first = randint(0, new_state.n - 1)
        second = randint(0, new_state.n - 1)
        while first == second:
            second = randint(0, new_state.n - 1)
        if repr(first)+"-"+repr(second) not in self.swap:
            self.swap[repr(first)+"-"+repr(second)] = True
            switch_people(first, second, new_state)
            yield (0, new_state)

    def value(self, state):
        res = 0
        for table in state.tables:
            for e1 in table:
                for e2 in table:
                    if e1 != e2:
                        res += state.m[e1][e2]
        return res
###############
# State class #
###############


class State:
    def __init__(self, n, t, m, tables, value):
        '''
        n is the number of guests
        t is the number of tables
        m is the affinity table
        tables is a representation of the tables
        value is the value of this state
        '''
        self.n = n
        self.t = t
        self.m = m
        self.tables = tables
        self.value = value

    def __str__(self):
        res = repr(self.value) + "\n"
        for table in self.tables:
            res += repr(table) + "\n"
        return res

    def __repr__(self):
        res = repr(self.value) + "\n"
        for table in self.tables:
            res += repr(table) + "\n"
        return res

################
# Local Search #
################


def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    list_of_best = []
    list_of_best_values = []
    for step in range(limit):
        if callback is not None:
            callback(current)
        for elem in list(current.expand()):
            if len(list_of_best) < 5:
                list_of_best.append(elem)
                list_of_best_values.append(elem.value())
            elif elem.value() > min(list_of_best_values):
                m = min(list_of_best_values)
                ind = list_of_best_values.index(m)
                list_of_best[ind] = elem
                list_of_best_values[ind] = elem.value()
    seed(42)
    return choice(list_of_best)

def maxvalue(problem, limit=100, callback=None):
    """Perform a random walk in the search space and return the best solution
    found. The returned value is a Node.
    If callback is not None, it must be a one-argument function that will be
    called at each step with the current node.
    """
    pass

if __name__ == '__main__':
    wedding = Wedding(sys.argv[1])
    print(wedding.initial)

    node = randomized_maxvalue(wedding, 100)
    # node = maxvalue(wedding, 100)
    #node = random_walk(wedding, limit=30)

    state = node.state
    print(state)
