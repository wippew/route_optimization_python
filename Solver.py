import pulp

from DrawOnMap import draw_on_map


def solveAndDraw(df, duration, task_count, vehicle_capacity, depots, depot_count, vehicle_count, types):
    # definition of LpProblem instance
    problem = pulp.LpProblem("VRP", pulp.LpMaximize)

    # definition of variables which are 0/1
    x = [[[pulp.LpVariable("x%s_%s" % (i, j), cat="Binary") if i != j else None for k in range(vehicle_count)] for
          j in range(task_count)] for i in range(task_count)]

    # add objective function maximize x
    problem += pulp.lpSum(x[i][j][k] if i != j else 0
                          for k in range(vehicle_count)
                          for j in range(task_count)
                          for i in range(task_count))
    # CONSTRAINTS
    # formula 1
    # constraint 1: Leave every task at most once
    for j in range(depot_count, task_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0
                              for i in range(task_count)
                              for k in range(vehicle_count)) <= 1
    # constraint 2: reach every task from at most one other task
    for i in range(depot_count, task_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0
                              for j in range(task_count)
                              for k in range(vehicle_count)) <= 1

    #//constraint 3: depart from own depot and return
    # depart from own depot and return to own depot
    for depot_index in range(depot_count):
        # for each car in each garage add constraint
        cars = depots[depot_index]
        for k in range(len(cars)):
            car = cars[k]
            problem += pulp.lpSum(x[depot_index][j][car] for j in range(task_count)) == 1
            problem += pulp.lpSum(x[i][depot_index][car] for i in range(task_count)) == 1

    #//constraint 4: no trip is conducted by a vehicle not belonging to a depot
    for depot_index in range(depot_count):
        cars = depots[depot_index]
        for other_depot in range(0, depot_count):
            if other_depot != depot_index:
                for k in range(len(cars)):
                    car = cars[k]
                    problem += pulp.lpSum(x[other_depot][j][car] for j in range(task_count)) == 0
                    problem += pulp.lpSum(x[i][other_depot][car] for i in range(task_count)) == 0


    # //constraint 5: number of vehicles in and out of a tasks's location stays the same
    for k in range(vehicle_count):
        for j in range(task_count):
            problem += pulp.lpSum(x[i][j][k] if i != j else 0
                                  for i in range(task_count)) - pulp.lpSum(
                x[j][i][k] for i in range(task_count)) == 0

    # //constraint 6: the time-capacity of each vehicle should not exceed the maximum capacity
    #for k in range(vehicle_count):
            # problem += pulp.lpSum(
            #     (duration[i][j] + df.demand[j]) * x[i][j][k] if i != j else 0 for i in range(task_count) for j in
    #  range(task_count)) <= vehicle_capacity


    t = pulp.LpVariable.dicts("t", (i for i in range(depot_count, task_count)), \
                              lowBound=1, upBound= task_count, cat='Continuous')
    # formula 5
    #eliminate subtour
    for i in range(depot_count, task_count):
        for j in range(depot_count, task_count):
            for k in range(vehicle_count):
                if i != j:
                    problem += t[j] >= t[i] + 1 - task_count * (1-x[i][j][k])

    # # first geometric constraint
    # for i in range(task_count):
    #     for j in range(task_count):
    #         for k in range(vehicle_count):
    #             if i != j:
    #                 problem += duration[i][j] * x[i][j][k] <= (45 * 60)

    # print vehicle_count which needed for solving problem
    # print calculated minimum distance value
    solution = problem.solve()
    if solution == 1:
        print('Vehicle Requirements:', vehicle_count)
        print('Nodes visited:', pulp.value(problem.objective))


    draw_on_map(df, depot_count, task_count, vehicle_count, x, types, t)
