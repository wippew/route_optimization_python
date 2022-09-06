import numpy as np
import pandas as pd
import pulp
import itertools
import gmaps
import googlemaps
import matplotlib.pyplot as plt
# from IPython.display import display

API_KEY = 'AIzaSyA28cLHKbm5apdM41K2Q7Nn3nXNToRzHSo'
gmaps.configure(api_key=API_KEY)
googlemaps = googlemaps.Client(key=API_KEY)

# customer count ('0' is depot)
customer_count = 6

# the number of vehicle
vehicle_count = 2

# the capacity of vehicle
vehicle_capacity = 480

# fix random seed
np.random.seed(seed=777)

# set depot latitude and longitude
depot_latitude = 40.748817
depot_longitude = -73.985428



# make dataframe which contains maintenance location and demand
df = pd.DataFrame({"latitude": np.random.normal(depot_latitude, 0.007, customer_count),
                   "longitude": np.random.normal(depot_longitude, 0.007, customer_count),
                   "demand": np.random.randint(10, 20, customer_count)})


# update depot values to correct places
df.at[0, "demand"] = 0
df.at[0, "latitude"] = depot_latitude
df.at[0, "longitude"] = depot_longitude

# function for calculating distance between two pins
def _duration_calculator(_df):
    _duration_result = np.zeros((len(_df), len(_df)))
    _df['latitude-longitude'] = '0'
    for i in range(len(_df)):
        _df['latitude-longitude'].iloc[i] = str(_df.latitude[i]) + ',' + str(_df.longitude[i])

    for i in range(len(_df)):
        for j in range(len(_df)):
            # calculate distance of all pairs
            _google_maps_api_result = googlemaps.directions(_df['latitude-longitude'].iloc[i],
                                                            _df['latitude-longitude'].iloc[j],
                                                            mode='driving')

            _duration_result[i][j] = _google_maps_api_result[0]['legs'][0]['duration']['value']

    return _duration_result


distance = _duration_calculator(df)


# definition of LpProblem instance
problem = pulp.LpProblem("CVRP", pulp.LpMinimize)

# definition of variables which are 0/1
x = [[[pulp.LpVariable("x%s_%s,%s" % (i, j, k), cat="Binary") if i != j else None for k in range(vehicle_count)] for
      j in range(customer_count)] for i in range(customer_count)]

# add objective function
problem += pulp.lpSum(distance[i][j] * x[i][j][k] if i != j else 0
                      for k in range(vehicle_count)
                      for j in range(customer_count)
                      for i in range(customer_count))

# constraints
# formula 1
for j in range(1, customer_count):
    problem += pulp.lpSum(x[i][j][k] if i != j else 0
                          for i in range(customer_count)
                          for k in range(vehicle_count)) == 1

    # foluma (3)
for k in range(vehicle_count):
    problem += pulp.lpSum(x[0][j][k] for j in range(1, customer_count)) == 1
    problem += pulp.lpSum(x[i][0][k] for i in range(1, customer_count)) == 1

# foluma (4)
for k in range(vehicle_count):
    for j in range(customer_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0
                              for i in range(customer_count)) - pulp.lpSum(
            x[j][i][k] for i in range(customer_count)) == 0

# foluma (5)
for k in range(vehicle_count):
    problem += pulp.lpSum(df.demand[j] * x[i][j][k] if i != j else 0 for i in range(customer_count) for j in
                          range(1, customer_count)) <= vehicle_capacity

    # fomula (6)
subtours = []
for i in range(2, customer_count):
    subtours += itertools.combinations(range(1, customer_count), i)

for s in subtours:
    problem += pulp.lpSum(
        x[i][j][k] if i != j else 0 for i, j in itertools.permutations(s, 2) for k in range(vehicle_count)) <= len(
        s) - 1

# print vehicle_count which needed for solving problem
# print calculated minimum distance value
if problem.solve() == 1:
    print('Vehicle Requirements:', vehicle_count)
    print('Moving Distance:', pulp.value(problem.objective))


# visualization : plotting with matplolib
plt.figure(figsize=(8, 8))
for i in range(customer_count):
    if i == 0:
        plt.scatter(df.latitude[i], df.longitude[i], c='green', s=200)
        plt.text(df.latitude[i], df.longitude[i], "depot", fontsize=12)
    else:
        plt.scatter(df.latitude[i], df.longitude[i], c='orange', s=200)
        plt.text(df.latitude[i], df.longitude[i], str(df.demand[i]), fontsize=12)

for k in range(vehicle_count):
    for i in range(customer_count):
        for j in range(customer_count):
            if i != j and pulp.value(x[i][j][k]) == 1:
                plt.plot([df.latitude[i], df.latitude[j]], [df.longitude[i], df.longitude[j]], c="black")

plt.show()