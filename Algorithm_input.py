import numpy as np
import pandas as pd

import Utils

from Utils import saveDistanceMatrixToFile, loadDistanceMatrixFromFile
from DurationService import duration_calculator
from Solver import solveAndDraw

customer_count = 16
# the number of vehicle
# vehicle_count = 2
# the capacity of vehicle
# 5h in seconds
vehicle_capacity = 4 * 3600
# fix random seed
np.random.seed(seed=456)
# set depot latitude and longitude
depot_latitude = 60.2031430359331
depot_longitude = 24.831880137248284

depot_2_latitude = 60.18949602985186
depot_2_longitude = 24.917047352139903


# make dataframe which contains maintenance location and demand
quarter_customer_count = int(customer_count/2)

# #lat
# lol1 = np.random.normal(depot_latitude, 0.005, quarter_customer_count)
# #long
# lol2 = np.random.normal(depot_longitude, 0.02, quarter_customer_count)
#
# #lat
# lol3 = np.random.normal(depot_2_latitude, 0.005, quarter_customer_count)
# #long
# lol4 = np.random.normal(depot_2_longitude, 0.01, quarter_customer_count)
#
#
# lol_first = np.concatenate((lol1, lol3))
# lol_second = np.concatenate((lol2, lol4))


df = pd.DataFrame({"latitude": np.random.normal(depot_latitude, 0.005, customer_count),
                   "longitude": np.random.normal(depot_longitude, 0.02, customer_count),
                   "demand": 60 * 60})

# update depot values to correct places
df.at[0, "demand"] = 0
df.at[0, "latitude"] = depot_latitude
df.at[0, "longitude"] = depot_longitude

df.at[1, "demand"] = 0
df.at[1, "latitude"] = depot_2_latitude
df.at[1, "longitude"] = depot_2_longitude

file_name = "test_file_%s.npy" % customer_count

fetch_new = 0

if fetch_new == 1:
    duration = duration_calculator(df)
    save = saveDistanceMatrixToFile(file_name, duration)
else:
    duration = loadDistanceMatrixFromFile(file_name)
    average2 = Utils.averageWithoutZeros(duration)
    solveAndDraw(df, duration, customer_count, vehicle_capacity)





