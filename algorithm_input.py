import numpy as np
import pandas as pd
from Utils import saveDistanceMatrixToFile, loadDistanceMatrixFromFile
from durationService import duration_calculator
from solver import solveAndDraw

# customer count ('0' is depot)
customer_count = 20
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
depot_2_latitude = 60.18289513777758
depot_2_longitude = 24.831880137248284

# make dataframe which contains maintenance location and demand
df = pd.DataFrame({"latitude": np.random.normal(depot_latitude, 0.02, customer_count),
                   "longitude": np.random.normal(depot_longitude, 0.02, customer_count),
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

duration = duration_calculator(df)

save = saveDistanceMatrixToFile(duration)

#duration = loadDistanceMatrixFromFile()

solveAndDraw(df, duration, customer_count, vehicle_count, vehicle_capacity)
