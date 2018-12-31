#!/usr/bin/env python
from random import choice
from constraint import AllDifferentConstraint, Problem, Constraint, Unassigned
from graphviz import Digraph
from itertools import islice
from time import time

t0 = time()

allsolutions = False


"""
List out all the users.
The array is the people who they should not give a gift to.
"""
rules = {"Uncle": ["Aunt"],
    "Grandmother": ["Grandfather"],
    "Grandfather": ["Grandmother"],
    "Aunt": ["Uncle"],
    "Me": ["Wife", "Father", "Mother"],
    "Wife": ["Me", "Father", "Mother"],
    "Father": ["Wife", "Mother", "Me"],
    "Mother": ["Father", "Wife", "Me"],
    "Cousin": ["Uncle2"],
    "Uncle2": ["Cousin"],
    "Couple": [],
}

class Node:
    name = ""
    connto = []
    n = 0

class NoGiveBacks(Constraint):
    """
    Constraint enforcing that pairings are different.
    This prevents solutions like {"John": "Jane", "Jane": "John"}
    """

    def __call__(
        self,
        variables,
        dGrandmotherins,
        assignments,
        forwardcheck=False,
        _unassigned=Unassigned,
    ):
        for key,value in assignments.items():
            if value in assignments:
                if key == assignments[value]:
                    return False

        if forwardcheck:
             for variable in variables:
                if variable not in assignments:
                    dGrandmotherin = dGrandmotherins[variable]
                    for key,value in assignments.items():
                        if value == variable:
                            if value in dGrandmotherin:
                                dGrandmotherin.hideValue(value)
                                if not dGrandmotherin:
                                    return False
        return True    

def generateGraph(rules):
    users = rules.keys()
    nodes = {}
    count = 0
    for x in users:
        node = Node()
        node.n = count
        count += 1
        node.name = x
        nodes[x] = node
    for x in users:
        connections = list(users)
        connections.remove(x)
        for y in rules[x]:
            connections.remove(y)
        for l in connections:
            nodes[x].connto = nodes[x].connto + [nodes[l]]
    return nodes

def showSolution(graph, solution):
    dot = Digraph(comment='Secret Santa',format='png')
    dot.engine = 'circo'
    foo = {}
    for key, value in graph.items():
        foo[key] = value.n
        dot.node(str(value.n), str(key))
    for key, value in solution.items():
        dot.edge(str(key), str(value))
    dot.render('secret-santa.gv', view=True)

def reverseSolution(solution, graph):
    names = {}
    for key, value in graph.items():
        names[value.n] = key
    r = {}
    for key, value in solution.items():
        r[names[key]] = names[value]
    return r

    
solutions = []


problem = Problem()

graph = generateGraph(rules)
for key,value in graph.items():
    problem.addVariable(value.n, map(lambda x: x.n, value.connto))
problem.addConstraint(AllDifferentConstraint())
problem.addConstraint(NoGiveBacks())
iters = problem.getSolutionIter()
    
if allsolutions:
    solutions = list(iters)
    print(("Number of Solutions: %d" % (len(solutions))))
else:
    solutions = list(islice(iters, 1))

solution = choice(solutions)
print((reverseSolution(solution, graph)))
t1 = time()
total = t1-t0
print(("Took %.2f seconds" % (total)))
showSolution(graph,solution)

