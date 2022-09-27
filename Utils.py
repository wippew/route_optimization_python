from tempfile import TemporaryFile
import numpy as np

# save duration service to file for development purposes only
def saveDistanceMatrixToFile(distanceMatrix):
    np.save('test_file_20.npy', distanceMatrix)


def loadDistanceMatrixFromFile():
    test = np.load('test_file_20.npy')
    return test

