from tempfile import TemporaryFile
import numpy as np

# save duration service to file for development purposes only
def saveDistanceMatrixToFile(filename ,distanceMatrix):
    np.save(filename, distanceMatrix)


def loadDistanceMatrixFromFile(filename):
    test = np.load(filename)
    return test


def average(lst):
    return sum(lst) / len(lst)

def averageWithoutZeros(lst):
    cell_total = list()
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            if i != j:
                cell_total.append(lst[i][j])

    return average(cell_total)

# def addNewDepots(depots, count):
#     for i in range(0, count):
#         depots.append([])
#
#
# def addVehicleToDepot(depots, depot, vehicle):
#     if depots[depot]:
#         depots[depot].append(vehicle)
#     else:
#         addNewDepot(depots)

def latlon_to_xy(lat, lon, src='epsg:4326'):
    import pyproj
    # in:  lat,lon as numpy arrays (dd.dddd, WGS84 default)
    # out: x,y as numpy arrays (ETRS-TM35FIN)

    proj_latlon = pyproj.Proj(init=src)  # default: WGS84
    proj_etrs = pyproj.Proj(init='epsg:3067')  # ETRS-TM35FIN

    return pyproj.transform(proj_latlon, proj_etrs, lon, lat)

def xy_to_latlon(x, y, src='epsg:4326'):
    # in:  x,y as numpy arrays (ETRS-TM35FIN)
    # out: lat,lon as numpy arrays (dd.ddd, WGS84 default)
    #      (might also be lon,lat...)
    import pyproj

    proj_latlon = pyproj.Proj(init=src) # default: WGS84
    proj_etrs = pyproj.Proj(init='epsg:3067') # ETRS-TM35FIN

    return pyproj.transform(proj_etrs, proj_latlon, x, y)