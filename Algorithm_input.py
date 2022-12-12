import pandas as pd

import Utils
from TaskService import create_node_coordinates, mock_node_coordinates

from Utils import saveDistanceMatrixToFile, loadDistanceMatrixFromFile
from DurationService import duration_calculator, get_travel_times_as_matrix
from Solver import solveAndDraw

depots = [[0]]
depot_count = len(depots)
vehicle_count = 0
for i in range(depot_count):
    vehicle_count += len(depots[i])

task_count = 3
total_count = depot_count + task_count

vehicle_capacity = 6 * 3600

x_coords, y_coords, demand, types = create_node_coordinates(task_count)
#x_coords, y_coords = mock_node_coordinates(task_count)

df = pd.DataFrame({"latitude": x_coords,
                   "longitude": y_coords,
                   "demand": 60 * 60})

file_name = "test_file_%s.npy" % total_count

fetch_new = 0


if fetch_new == 1:
    duration = get_travel_times_as_matrix(df)
    save = saveDistanceMatrixToFile(file_name, duration)
else:
    duration = loadDistanceMatrixFromFile(file_name)
    duration[0][0] = 0.0;
    duration[0][1] = 10.0;
    duration[0][2] = 10.0;
    duration[0][3] = 10.0;
    duration[1][1] = 0.0;
    duration[1][0] = 10.0;
    duration[1][2] = 10.0;
    duration[1][3] = 10.0;
    duration[2][2] = 0.0;
    duration[2][0] = 10.0;
    duration[2][1] = 10.0;
    duration[2][3] = 10.0;
    duration[3][3] = 0.0;
    duration[3][0] = 10.0;
    duration[3][1] = 10.0;
    duration[3][2] = 10.0;
    df.demand[0] = 0

    solveAndDraw(df, duration, total_count, vehicle_capacity, depots, depot_count, vehicle_count, types)





