import pandas as pd

import Utils
from TaskService import create_node_coordinates, mock_node_coordinates

from Utils import saveDistanceMatrixToFile, loadDistanceMatrixFromFile
from DurationService import duration_calculator, get_travel_times_as_matrix
from Solver import solveAndDraw

depots = [[0,1]]
depot_count = len(depots)
vehicle_count = 0
for i in range(depot_count):
    vehicle_count += len(depots[i])




task_count = 20
total_count = depot_count + task_count

vehicle_capacity = 6 * 3600

x_coords, y_coords, demand, types = create_node_coordinates(task_count)
#x_coords, y_coords = mock_node_coordinates(task_count)

df = pd.DataFrame({"latitude": x_coords,
                   "longitude": y_coords,
                   "demand": 60 * 60})

file_name = "test_file_%s.npy" % total_count

fetch_new =0


if fetch_new == 1:
    duration = get_travel_times_as_matrix(df)
    save = saveDistanceMatrixToFile(file_name, duration)
else:
    duration = loadDistanceMatrixFromFile(file_name)
    solveAndDraw(df, duration, total_count, vehicle_capacity, depots, depot_count, vehicle_count, types)





