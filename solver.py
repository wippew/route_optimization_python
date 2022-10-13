import itertools

import pulp
import matplotlib.pyplot as plt


def solveAndDraw(df, duration, task_count, vehicle_count, vehicle_capacity):

    depots = [[0], [1]]
    depot_count = len(depots)
    vehicle_count = 2

    # definition of LpProblem instance
    problem = pulp.LpProblem("VRP", pulp.LpMaximize)

    # definition of variables which are 0/1
    x = [[[pulp.LpVariable("x%s_%s,%s" % (i, j, k), cat="Binary") if i != j else None for k in range(vehicle_count)] for
          j in range(task_count)] for i in range(task_count)]

    # add objective function maximize x
    problem += pulp.lpSum(x[i][j][k] if i != j else 0
                          for k in range(vehicle_count)
                          for j in range(task_count)
                          for i in range(task_count))
    # CONSTRAINTS
    # formula 1
    # only one visit per task location
    for j in range(depot_count, task_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0
                              for i in range(task_count)
                              for k in range(vehicle_count)) <= 1

    for i in range(depot_count, task_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0
                              for j in range(task_count)
                              for k in range(vehicle_count)) <= 1

    # formula 2
    # depart from own depot and return to own depot
    for depot_index in range(depot_count):
        # for each car in each garage add constraint
        cars = depots[depot_index]
        for k in range(len(cars)):
            car = cars[k]
            problem += pulp.lpSum(x[depot_index][j][car] for j in range(task_count)) == 1
            problem += pulp.lpSum(x[i][depot_index][car] for i in range(task_count)) == 1

    #formula 3, no trip is conducted by a vehicle not belonging to a depot
    for depot_index in range(depot_count):
        cars = depots[depot_index]
        for other_depot in range(0, depot_count):
            if other_depot != depot_index:
                for k in range(len(cars)):
                    car = cars[k]
                    problem += pulp.lpSum(x[other_depot][j][car] for j in range(task_count)) == 0
                    problem += pulp.lpSum(x[i][other_depot][car] for i in range(task_count)) == 0


    # formula 3
    # number of vehicles in and out of a task's location stays the same
    for k in range(vehicle_count):
        for j in range(task_count):
            problem += pulp.lpSum(x[i][j][k] if i != j else 0
                                  for i in range(task_count)) - pulp.lpSum(
                x[j][i][k] for i in range(task_count)) == 0

    # formula 4
    # the time-capacity of each vehicle should not exceed the maximum capacity
    for k in range(vehicle_count):
        problem += pulp.lpSum(
            (duration[i][j] + df.demand[j]) * x[i][j][k] if i != j else 0 for i in range(task_count) for j in
            range(depot_count, task_count)) <= vehicle_capacity


    t = pulp.LpVariable.dicts("t", (i for i in range(task_count)), \
                              lowBound=1, upBound= task_count, cat='Continuous')
    # formula 5
    #eliminate subtour
    for i in range(depot_count, task_count):
        for j in range(depot_count, task_count):
            for k in range(vehicle_count):
                if i != j:
                    problem += t[j] >= t[i] + 1 - 5 * (1-x[i][j][k])

    #Old eliminate subtour
    # subtours = []
    # for i in range(2, task_count):
    #     subtours += itertools.combinations(range(1, task_count), i)
    #
    # for s in subtours:
    #     problem += pulp.lpSum(
    #         x[i][j][k] if i != j else 0 for i, j in itertools.permutations(s, 2) for k in range(vehicle_count)) <= len(s) - 1

    # formula 6
    # no inter depot tour
    # for k in range(vehicle_count):
    #     for i in range(0, depot_count):
    #         for j in range(0, depot_count):
    #             if i != j:
    #                 problem += x[i][j][k] == 0

    # first geometric constraint
    # for i in range(task_count):
    #     for j in range(task_count):
    #         for k in range(vehicle_count):
    #             if i != j:
    #                 problem += duration[i][j] * x[i][j][k] <= (4 * 60)

    # print vehicle_count which needed for solving problem
    # print calculated minimum distance value
    solution = problem.solve()
    if solution == 1:
        print('Vehicle Requirements:', vehicle_count)
        print('Nodes visited:', pulp.value(problem.objective))

    # visualization : plotting with matplolib
    plt.figure(figsize=(8, 8))
    for i in range(task_count):
        if i == 0:
            plt.scatter(df.longitude[i], df.latitude[i], c='green', s=100)
            plt.text(df.longitude[i], df.latitude[i], "depot" + str(i), fontsize=12)
        elif i == 1:
            plt.scatter(df.longitude[i], df.latitude[i], c='red', s=100)
            plt.text(df.longitude[i], df.latitude[i], "depot_2"+ str(i), fontsize=12)
        else:
            plt.scatter(df.longitude[i], df.latitude[i], c='orange', s=50)
            plt.text(df.longitude[i], df.latitude[i], str(i), fontsize=12)

    colors = ["red", "blue", "black", "orange", "gray"]
    k0 = []
    k1 = []
    for k in range(vehicle_count):
        for i in range(task_count):
            for j in range(task_count):
                if i != j and pulp.value(x[i][j][k]) == 1:
                    if k == 0:
                        plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="green")
                        k0.append("%s_%s" % (i, j))
                    elif k == 1:
                        plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="red")
                        k1.append("%s_%s" % (i, j))
                    elif k == 2:
                        plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="gray")
                    else:
                        plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="green")

    print("the array is: ", k0)
    print("the array is: ", k1)
    plt.show()

