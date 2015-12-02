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


def get_init_state_from_file(filename):
    number_participants = 0
    number_tables = 0
    grid = {}
    tables = []
    value = 0
    with open(filename, 'r') as f:
        # read_data = f.read()
        number_participants = int(f.readline())
        number_tables = int(f.readline())
        number_participants_by_table = int(
            number_participants / number_tables)
        i = 0
        for line in f:
            grid[i] = [int(i) for i in line.split()]
            i += 1
        assigned_people = {}
        i = 0
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
    return State(number_participants, number_tables, grid, tables, value)

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

class Wedding(Problem):

    def __init__(self, init):
        #self.old_tables = {}
        #self.best_value = 0

        Problem.__init__(self, get_init_state_from_file(init))

    def switch_people(self, person1, person2, state):
        '''
        Changes the state by switching person1
        and person2 in the tables they are assigned
        to.
        The tables will be changed, the value of the state will be updated.
        '''
        table1 = None
        t_ind1 = -1
        p_ind1 = -1
        table2 = None
        p_ind2 = -1
        t_ind2 = -1
        new_tables = deepcopy(state.tables)
        # Récupère les gens dans les tables
        for i in range(len(state.tables)):
            if table1 == None:
                try:
                    p_ind1 = new_tables[i].index(person1)
                    table1 = new_tables[i]
                    t_ind1 = i
                except ValueError as _:
                    pass
            if table2 == None:
                try:
                    p_ind2 = new_tables[i].index(person2)
                    table2 = new_tables[i]
                    t_ind2 = i
                except ValueError as _:
                    pass
            if table1 != None and table2 != None:
                break

        # Calcule l'ancienne valeur d'affinité
        old_value = table_value(
            table1, state.m) + table_value(table2, state.m)
        # switch des gens
        new_tables[t_ind1][p_ind1] = person2
        new_tables[t_ind1] = sorted(new_tables[t_ind1])
        new_tables[t_ind2][p_ind2] = person1
        new_tables[t_ind2] = sorted(new_tables[t_ind2])
        # print(state.tables)
        # calcul de la nouvelle valeur de l'affinité
        new_value = table_value(
            new_tables[t_ind1], state.m) + table_value(new_tables[t_ind2], state.m)

        #if (self.best_value < state.value - old_value + new_value):
        #    self.best_value = state.value - old_value + new_value
        #    print(repr(self.best_value))

        return State(state.n, state.t, state.m, new_tables, state.value - old_value + new_value)

    def successor(self, state):
        swap = {}
        #if self.old_tables == state.tables:
            #print('wtf')
        self.old_tables = state.tables
        for table in state.tables:
            for e1 in table:
                for table2 in state.tables:
                    if table != table2:
                        for e2 in table2:
                            if (e1, e2) not in swap:
                                swap[(e1, e2)] = True
                                swap[(e2, e1)] = True
                                yield (0, self.switch_people(e1, e2, state))

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
        res = repr(self.value)
        for table in self.tables:
            res += "\n"
            for e in table:
                res += repr(e) + " "
            res = res.strip()
        return res

    def __repr__(self):
        res = repr(self.value) + "\n"
        for table in self.tables:
            for e in table:
                res += repr(e)
            res += "\n"
        return res

    def __lt__(self, other):
        res = False
        self_concat = []
        other_concat = []
        for i in range(len(self.tables)):
            self_concat += self.tables[i]
            other_concat += other.tables[i]
        if self_concat >= other_concat:
            return False
        return True

    def __le__(self, other):
        res = False
        self_concat = []
        other_concat = []
        for i in range(len(self.tables)):
            self_concat += self.tables[i]
            other_concat += other.tables[i]
        if self_concat > other_concat:
            return False
        return True

    def __eq__(self, other):
        res = False
        self_concat = []
        other_concat = []
        for i in range(len(self.tables)):
            self_concat += self.tables[i]
            other_concat += other.tables[i]
        if self_concat != other_concat:
            return False
        return True

    def __ne__(self, other):
        res = False
        self_concat = []
        other_concat = []
        for i in range(len(self.tables)):
            self_concat += self.tables[i]
            other_concat += other.tables[i]
        if self_concat == other_concat:
            return False
        return True

    def __gt__(self, other):
        res = False
        self_concat = []
        other_concat = []
        for i in range(len(self.tables)):
            self_concat += self.tables[i]
            other_concat += other.tables[i]
        if self_concat <= other_concat:
            return False
        return True

    def __ge__(self, other):
        res = False
        self_concat = []
        other_concat = []
        for i in range(len(self.tables)):
            self_concat += self.tables[i]
            other_concat += other.tables[i]
        if self_concat < other_concat:
            return False
        return True

################
# Local Search #
################


def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    seed(42)
    list_of_best = []
    list_of_best_values = []
    for step in range(limit):
        list_of_best = []
        list_of_best_values = []
        if callback is not None:
            callback(current)
        for elem in list(current.expand()):
            if len(list_of_best) < 5:
                list_of_best.append(elem)
                list_of_best_values.append(elem.value())
            elif elem.value() > min(list_of_best_values):
                m = min(list_of_best_values)
                ind = list_of_best_values.index(m)
                # Remove the worst state by concat
                if list_of_best_values.count(m) > 1:
                    worst_node = list_of_best[ind]
                    for r in range(len(list_of_best_values)):
                        if list_of_best_values[r] == m:
                            if list_of_best[r].state < worst_node.state:
                                worst_node = list_of_best[r]
                                ind = r
                list_of_best[ind] = elem
                list_of_best_values[ind] = elem.value()
        current = choice(list_of_best)
    m = max(list_of_best_values)
    ind = list_of_best_values.index(m)
    best_node = list_of_best[ind]
    if list_of_best_values.count(m) > 1:
        for r in range(len(list_of_best_values)):
            if list_of_best_values == m:
                if best_node < list_of_best[r] :
                    best_node = list_of_best[r]

    return best_node


def maxvalue(problem, limit=100, callback=None):
    """Perform a random walk in the search space and return the best solution
    found. The returned value is a Node.
    If callback is not None, it must be a one-argument function that will be
    called at each step with the current node.
    """
    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        best._value = 0
        if callback is not None:
            callback(current)
        for elem in list(current.expand()):
            if elem.value() > best.value():
                best = elem
            elif elem.value() == best.value():
                if best.state >= elem.state:
                    best = elem
        current = best
    return best

if __name__ == '__main__':
    wedding = Wedding(sys.argv[1])
    print(wedding.initial)

    # node = randomized_maxvalue(wedding, 100)
    node = maxvalue(wedding, 100)
    # node = random_walk(wedding, limit=30)

    state = node.state
    print(state)
