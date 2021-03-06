#! /usr/bin/env python3
# coding: utf-8
##########################################################################
#
#		Implementation of the wedding problem class
#
##########################################################################
from search import Problem, LSNode, random_walk
from copy import deepcopy
from random import seed, choice
import sys

#################
# Problem class #
#################


def get_init_state_from_file(filename):
    '''
    Constructs the initial state of a Wedding problem.
    filename must be a valid path to a file
    return : a State containing every information needed
    '''
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
        new_tables = list(state.tables)
        # Récupère les gens dans les tables
        for i in range(len(state.tables)):
            if table1 == None:
                try:
                    p_ind1 = new_tables[i].index(person1)
                    table1 = state.tables[i]
                    new_tables[i] = list(table1)
                    t_ind1 = i
                except ValueError as _:
                    pass
            if table2 == None:
                try:
                    p_ind2 = new_tables[i].index(person2)
                    table2 = state.tables[i]
                    new_tables[i] = list(table2)
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

        '''
        if (self.best_value < state.value - old_value + new_value):
            self.best_value = state.value - old_value + new_value
            print('---------------------------')
            print(repr(old_value))
            print(repr(new_value))
            print(repr(self.best_value))
            print('---------------------------')
        '''
        return State(state.n, state.t, state.m, new_tables, state.value - old_value + new_value)

    def successor(self, state):
        swap = {}
        #if self.old_tables == state.tables:
        #    print('wtf')
        #self.old_tables = state.tables
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
        return state.value
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

    def __gt__(self, other):
        diff_value = self.value - other.value
        if diff_value == 0:
            self_concat = []
            other_concat = []
            for i in range(len(self.tables)):
                self_concat += self.tables[i]
                other_concat += other.tables[i]
            #    if self_concat < other_concat:
            #        return False
            #return True
            return self_concat < other_concat
        else:
            return self.value > other.value

################
# Local Search #
################


def randomized_maxvalue(problem, limit=100, callback=None):
    seed(42)
    current = LSNode(problem, problem.initial, 0)
    best = current
    for _ in range(limit):
        if callback is not None:
            callback(current)
        successors = list(current.expand())
        list_of_best = []
        i = 0
        while (i < 5):
            ind = successors.index(max(successors, key=lambda node: node.state))
            list_of_best.append(successors[ind])
            successors.pop(ind)
            i += 1
        current = choice(list_of_best)
        if current.state > best.state:
            best = current
    return best


def maxvalue(problem, limit=100, callback=None):
    """Perform a random walk in the search space and return the best solution
    found. The returned value is a Node.
    If callback is not None, it must be a one-argument function that will be
    called at each step with the current node.
    """
    current = LSNode(problem, problem.initial, 0)
    best_of_best = current
    #best.v = current.state.value
    for _ in range(limit):
        #best.v = -float('inf')
        if callback is not None:
            callback(current)
        successors = list(current.expand())
        ind = successors.index(max(successors, key=lambda node: node.state))
        current = successors[ind]
        if current.state > best_of_best.state:
            best_of_best = current
    #return current
    return best_of_best

if __name__ == '__main__':
    wedding = Wedding(sys.argv[1])
    print(wedding.initial)

    node = randomized_maxvalue(wedding, 100)
    # node = maxvalue(wedding, 100)
    # node = random_walk(wedding, limit=30)

    s = node.state
    print(s)
