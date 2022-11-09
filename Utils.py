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


def get_color_by_type(type):
    colors = ["red", "blue", "black", "orange", "gray"]
    if type == 'Rumputarkastus 1v':
        return 'red'
    elif type == 'Siltatarkastus 1v':
        return 'blue'
    elif type == 'Vaihde 2v huolto':
        return 'black'
    elif type == 'Opastinhuolto 12kk':
        return 'gray'
    elif type == 'Akselinlaskijahuolto 12 kk':
        return 'yellow'
    elif type == 'Kävelytarkastus 1 v kevät':
        return 'pink'
    elif type == 'Vaihde 2v huolto':
        return 'purple'
    elif type == 'Kaapit ja kojut 12kk':
        return 'orange'
    elif type == 'Liikennepaikkatarkastus 1v':
        return 'white'


def order_correctly(k0):
    # get first one first
    for i in k0:
        split = i.split(",")
        test = "asd"

    omfg = "asd"