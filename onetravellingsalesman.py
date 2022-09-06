import six
import sys
sys.modules['sklearn.externals.six'] = six

import mlrose
import numpy as np


expected_duration_for_task = 1

time_interval = 40
starting_point = "A"

tasks = [1, 2, 3, 4, 5]

# distances = {"AB": 10, "AC": 40, "AD": 10, "AE": 15, "AF": 60,
#              "BC": 30, "BD": 15, "BE": 10, "BF": 35,
#              "CD": 55, "CE": 35, "CF": 15,
#              "DE": 10, "DF": 45,
#              "EF":35}
start_and_end_point = 6

dist_list = [(0, 1, 10), (0, 2, 40), (0, 3, 10), (0, 4, 15), (0, 5, 60),
             (1, 2, 30), (1, 3, 15), (1, 4, 10), (1, 5, 35),
             (2, 3, 55), (2, 4, 35), (2, 5, 15),
             (3, 4, 10), (3, 5, 45),
             (4, 5, 35),
             (1, )]

fitness_dists = mlrose.TravellingSales(distances=dist_list)

problem_fit = mlrose.TSPOpt(length = 6, fitness_fn=fitness_dists, maximize=False)

best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state = 2)

print("the best state found is", best_state)

print("the fitness at the best state is", best_fitness)


#TBI
start_and_end_point = 0




