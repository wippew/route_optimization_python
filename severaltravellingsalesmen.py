import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cvxpy as cp
from geopy import distance
from cvxopt import glpk


points = [(60.243943676108124, 24.82135224831975),
          (60.26796040932812, 24.98889374874879),
          (60.21257618676047, 25.021509409402643),
          (60.19978191147801, 25.123819588597506),
          (60.16683502902986, 24.937738656653725),
          (60.16205242421368, 24.763330702860685),
          (60.24394367583073, 25.074037790566713)]

n = len(points)
C = np.zeros((n, n, n))

for i in range(0, n):
    for j in range(0, n):
        C[i, j] = distance.distance(points[i], points[j]).km

# Distance matrix
print("Distance matrix is: \n")
print(np.round(C, 4))

# startPoint munkkiranta
60.146162347520395, 24.672350175059044

################################################
# Solving the integer programming problem
################################################

# Defining the variables
X = cp.Variable(C.shape, boolean=True)
X_2 = cp.Variable((n, n), boolean=True)
u = cp.Variable(n, integer=True)
m = 3
ones = np.ones((n,1))

# Defining the objective function
objective = cp.Minimize(cp.sum(cp.multiply(C, X)))

# Defining the constraints
constraints = []
testing = X[0, :]
testing2 = X[0, :] @ ones

constraints += [X[0,:] @ ones == m]
constraints += [X[:,0] @ ones == m]
constraints += [X[1:,:] @ ones == 1]
constraints += [X[:,1:].T @ ones == 1]
constraints += [cp.diag(X) == 0]
constraints += [u[1:] >= 2]
constraints += [u[1:] <= n]
constraints += [u[0] == 1]

for i in range(1, n):
    for j in range(1, n):
        if i != j:
            constraints += [ u[i] - u[j] + 1  <= (n - 1) * (1 - X[i, j]) ]

# Solving the problem
prob = cp.Problem(objective, constraints)
prob.solve(verbose=False)

# Transforming the solution to paths
X_sol = np.argwhere(X.value==1)

ruta = {}
for i in range(0, m):
    ruta['Salesman_' + str(i+1)] = [0]
    j = i
    a = 10e10
    while a != 0:
        a = X_sol[j,1]
        ruta['Salesman_' + str(i+1)].append(a)
        j = np.where(X_sol[:,0] == a)
        j = j[0][0]
        a = j

# Showing the paths
for i in ruta.keys():
    print('The path of ' + i + ' is:\n')
    print( ' => '.join(map(str, ruta[i])))
    print('')

# Transforming the points to the xy plane approximately
xy_cords = np.zeros((n, 2))

for i in range(0, n):
    xy_cords[i, 0] = distance.distance((points[0][1], 0), (points[i][1], 0)).km
    xy_cords[i, 1] = distance.distance((0, points[0][0]), (0, points[i][0])).km

################################################
# Plotting the optimal path
################################################

# Plotting the points
fig, ax = plt.subplots(figsize=(14,7))

for i in range(n):
    ax.annotate(str(i), xy=(xy_cords[i,0], xy_cords[i,1]+0.1))

ax.scatter(xy_cords[:,0],xy_cords[:,1])
for i in ruta.keys():
    ax.plot(xy_cords[ruta[i],0], xy_cords[ruta[i],1], label = i)
    ax.legend(loc='best')

# Showing the optimal distance
distance = np.sum(np.multiply(C, X.value))
print('The optimal distance is:', np.round(distance,2), 'km')