from ast import Str
from cmath import inf
from math import dist
import random
import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose



class Node:
    def __init__(self, giver, receiver):
        self.giver = giver
        self.receiver = receiver

    def __str__(self):
        return self.giver + " beschenkt " + str(self.receiver)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.giver == other.giver and self.receiver == other.receiver


names = []
print("Trage die Namen deiner Mitbewohners ein. Schließe den Vorgang ab mit ENTER.")

while(True):
    input_string = input()
    if(input_string == ""):
        break
    names.append(input_string)

print("These were the names you chose: " + str(names))
if(len(names) < 3):
    print("You have to choose more than two names! QUIT")
    quit()

nodes = []
for giver in names:
    for receiver in names:
        if (giver != receiver):
            nodes.append(Node(giver, receiver))

while(len(nodes) > 24):
    nodes.remove(random.choice(nodes))


costs = []

for i in range(len(nodes)):
    for j in range(i, len(nodes)):
        A = nodes[i]
        B = nodes[j]
        if (A.giver == B.giver):
            continue
        if (A.receiver == B.receiver):
            continue
        if (A.giver == B.receiver and A.receiver == B.giver):
            continue

        if (A.giver != B.receiver and A.receiver != B.giver):
            costs.append((i,j,1))
        else:
            costs.append((i,j,2))

# for dist in costs:
#     print(str(nodes[dist[0]]) + " / " + str(nodes[dist[1]]) + " = " + str(dist[2]))


fitness_coords = mlrose.TravellingSales(distances=costs)

problem_fit = mlrose.TSPOpt(length = len(nodes), fitness_fn = fitness_coords, maximize=False)

best_state, best_fitness = mlrose.genetic_alg(problem_fit, pop_size=400, max_attempts=20, mutation_prob=0.1)


evaluation = []
for i in range(24):
    index = i % len(nodes)
    print("[" + str(i+1) + "]\t" + str(nodes[best_state[index]]))

for i in range(23):
    A = nodes[best_state[i % len(nodes)]]
    B = nodes[best_state[(i+1) % len(nodes)]]
    if (A.giver == B.giver or A.receiver == B.receiver or A.giver == B.receiver and A.receiver == B.giver):
        evaluation.append(2)
    if (A.giver == B.receiver or A.receiver == B.giver):
        evaluation.append(1)
    else:
        evaluation.append(0)

if(evaluation.count(2) > 0):
    print("This solution has " + str(evaluation.count(2)) + " days where the flip is bad.")
else:
    print("This solution has " + str(evaluation.count(1)) + " days where the flip is not optimal.")
