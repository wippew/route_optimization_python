import pulp
import itertools
import matplotlib.pyplot as plt
from durationService import duration_calculator


def solveAndDraw(df, duration, customer_count, vehicle_count, vehicle_capacity):
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

    for i in range(1, customer_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0
                              for j in range(customer_count)
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


    t = pulp.LpVariable.dicts("t", (i for i in range(customer_count)), \
                                 lowBound=1,upBound= customer_count, cat='Continuous')
    # formula 5
    #eliminate subtour
    for i in range(customer_count):
        for j in range(customer_count):
            for k in range(vehicle_count):
                if i != j and (i != 0 and j != 0):
                    problem += t[j] >= t[i] + 1 - (customer_count/3) * (1-x[i][j][k])

    # first geometric constraint
    for i in range(customer_count):
        for j in range(customer_count):
            for k in range(vehicle_count):
                if i != j:
                    problem += duration[i][j] * x[i][j][k] <= (30 * 60)

    # print vehicle_count which needed for solving problem
    # print calculated minimum distance value
    solution = problem.solve()
    if solution == 1:
        print('Vehicle Requirements:', vehicle_count)
        print('Moving Time:', pulp.value(problem.objective))

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