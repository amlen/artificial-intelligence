#! /usr/bin/env python3
##########################################################################
#
#		Implementation of the wedding problem class
#
##########################################################################
from search import Problem, LSNode
from random import random
import sys

#################
# Problem class #
#################


class Wedding(Problem):

    def __init__(self, init):
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
                grid[i] = results = [int(i) for i in line.split()]
                i += 1
            assigned_people = {}
            i = 0
            tables = []
            value = 0
            while (i < number_participants):
                if i not in assigned_people:
                    assigned_people[i] = True
                    cnt = 1
                    table = [i]
                    line = list(grid[i])
                    while (cnt < number_participants_by_table):
                        m = max(line)
                        ind = line.index(m)
                        if ind not in assigned_people:
                            assigned_people[ind] = True
                            table.append(ind)
                            cnt += 1
                        line[ind] = -sys.maxsize
                    for e1 in table:
                        for e2 in table:
                            value += grid[e1][e2]
                    tables.append(sorted(table))
                i += 1

            self.initial = State(
                number_participants, number_tables, grid, tables, value)

    def successor(self, state):

        pass

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


################
# Local Search #
################


def randomized_maxvalue(problem, limit=100, callback=None):
    pass


def maxvalue(problem, limit=100, callback=None):
    """Perform a random walk in the search space and return the best solution
    found. The returned value is a Node.
    If callback is not None, it must be a one-argument function that will be
    called at each step with the current node.
    """
    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        if callback is not None:
            callback(current)
        current = random.choice(list(current.expand()))
        if current.value() > best.value():
            best = current
    return best

if __name__ == '__main__':
    wedding = Wedding(sys.argv[1])
    print(wedding.initial)

    # node = randomized_maxvalue(wedding, 100)
    # node = maxvalue(wedding, 100)

    # state = node.state
    # print(state)
