from tempfile import TemporaryFile
import numpy as np

# save duration service to file for development purposes only
def saveDistanceMatrixToFile(filename ,distanceMatrix):
    np.save(filename, distanceMatrix)


def loadDistanceMatrixFromFile(filename):
    test = np.load(filename)
    return test


def Average(lst):
    return sum(lst) / len(lst)

def AverageWithoutZeros(lst):
    cell_total = list()
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            if i != j:
                cell_total.append(lst[i][j])

    return Average(cell_total)
