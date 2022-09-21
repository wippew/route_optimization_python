import numpy as np
import pandas as pd
import pulp
import itertools
import matplotlib.pyplot as plt
from Utils import saveDistanceMatrixToFile, loadDistanceMatrixFromFile
from durationService import duration_calculator

# customer count ('0' is depot)
customer_count = 10

# the number of vehicle
vehicle_count = 2

# the capacity of vehicle
# 5h in seconds
vehicle_capacity = 5 * 3600

# fix random seed
np.random.seed(seed=456)

# set depot latitude and longitude
depot_latitude = 60.18949602985186
depot_longitude = 24.917047352139903

#depot_2_latitude = 60.18289513777758
# depot_2_longitude = 24.831880137248284

# make dataframe which contains maintenance location and demand
df = pd.DataFrame({"latitude": np.random.normal(depot_latitude, 0.1, customer_count),
                   "longitude": np.random.normal(depot_longitude, 0.1, customer_count),
                   "demand": 60 * 60})

# update depot values to correct places
df.at[0, "demand"] = 0
df.at[0, "latitude"] = depot_latitude
df.at[0, "longitude"] = depot_longitude

# df.at[1, 'demand'] = 0

# otaniementie loc, depot t
df.latitude[1] = 60.18289513777758
df.longitude[1] = 24.831880137248284
# yhtiöntie 2 loc
df.latitude[2] = 60.2031430359331
df.longitude[2] = 24.721788777912327
# alppikatu
df.latitude[3] = 60.185696847692576
df.longitude[3] = 24.94451173724837

#duration = duration_calculator(df)

#save = saveDistanceMatrixToFile(duration)

duration = loadDistanceMatrixFromFile()

# definition of LpProblem instance
problem = pulp.LpProblem("VRP", pulp.LpMaximize)

# definition of variables which are 0/1
x = [[[pulp.LpVariable("x%s_%s,%s" % (i, j, k), cat="Binary") if i != j else None for k in range(vehicle_count)] for
      j in range(customer_count)] for i in range(customer_count)]

# add objective function maximize x
problem += pulp.lpSum(x[i][j][k] if i != j else 0
                      for k in range(vehicle_count)
                      for j in range(customer_count)
                      for i in range(customer_count))

# CONSTRAINTS
# formula 1
# only one visit per task location
for j in range(1, customer_count):
    problem += pulp.lpSum(x[i][j][k] if i != j else 0
                          for i in range(customer_count)
                          for k in range(vehicle_count)) <= 1

# formula 2
# depart from depot and return to depot
for k in range(vehicle_count):
    problem += pulp.lpSum(x[0][j][k] for j in range(1, customer_count)) == 1
    problem += pulp.lpSum(x[i][0][k] for i in range(1, customer_count)) == 1

# formula 3
# number of vehicles in and out of a task's location stays the same
for k in range(vehicle_count):
    for j in range(customer_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0
                              for i in range(customer_count)) - pulp.lpSum(
            x[j][i][k] for i in range(customer_count)) == 0

# formula 4
# the time-capacity of each vehicle should not exceed the maximum capacity
for k in range(vehicle_count):
    problem += pulp.lpSum(
        (duration[i][j] + df.demand[j]) * x[i][j][k] if i != j else 0 for i in range(customer_count) for j in
        range(1, customer_count)) <= vehicle_capacity

# formula 5
# removal of subtours
subtours = []
for i in range(2, customer_count):
    subtours += itertools.combinations(range(1, customer_count), i)

for s in subtours:
    problem += pulp.lpSum(
        x[i][j][k] if i != j else 0 for i, j in itertools.permutations(s, 2) for k in range(vehicle_count)) <= len(
        s) - 1

# print vehicle_count which needed for solving problem
# print calculated minimum distance value
solution = problem.solve()
if solution == 1:
    print('Vehicle Requirements:', vehicle_count)
    print('Moving Distance:', pulp.value(problem.objective))

testing = pulp.LpStatus[solution]

# visualization : plotting with matplolib
plt.figure(figsize=(8, 8))
for i in range(customer_count):
    if i == 0:
        plt.scatter(df.longitude[i], df.latitude[i], c='green', s=200)
        plt.text(df.longitude[i], df.latitude[i], "depot", fontsize=12)
    else:
        plt.scatter(df.longitude[i], df.latitude[i], c='orange', s=200)
        plt.text(df.longitude[i], df.latitude[i], str(df.demand[i] / 60), fontsize=12)

colors = ["red", "blue", "black", "orange", "gray"]
for k in range(vehicle_count):
    for i in range(customer_count):
        for j in range(customer_count):
            if i != j and pulp.value(x[i][j][k]) == 1:
                if k == 0:
                    plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="black")
                elif k == 1:
                    plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="red")
                else:
                    plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="green")
plt.show()
