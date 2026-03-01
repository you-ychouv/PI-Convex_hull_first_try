import numpy as np
import matplotlib.pyplot as plt
import random


def datasetB(n):
  a = np.array(np.random.uniform(0,1,n))
  b = np.array(np.random.uniform(0,1,n))
  point = []
  for i in range(0,n):
    k = np.array((a[i], b[i]))
    point.append(k)
  return point

# Testing
print(datasetB(7))
dataB = datasetB(1000)
for i in range(len(dataB)):
  plt.scatter(dataB[i][0], dataB[i][1])
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

def datasetA(n):
  if n < 4:
    return []
  point = datasetB(n-4)
  point.append(np.array((0, 0)))
  point.append(np.array((0, 1)))
  point.append(np.array((1, 0)))
  point.append(np.array((1, 1)))

  # rotation
  alpha = np.pi/6 # we can choose any other angle, we take pi/6 here as an random example.
  rotated_points = []
  for i in point:
    r = np.sqrt(i[0]**2 + i[1]**2)
    if r == 0:
      rotated_points.append(np.array([0.0, 0.0]))
    else:
      alpha_P = np.arctan2(i[1], i[0])
      x = r * np.cos(alpha_P - alpha)
      y = r * np.sin(alpha_P - alpha)
      rotated_points.append(np.array([float(x), float(y)]))

  # shuffle
  np.random.shuffle(rotated_points)

  return rotated_points

# tesing
print (datasetA(1000))
point = datasetA(1000)
for i in range(len(point)):
  plt.scatter(point[i][0], point[i][1])
plt.gca().set_aspect('equal', adjustable='box')
plt.show()


def datasetC(n):
  point = datasetB(n)
  pointC = []
  center = np.array((0.5, 0.5))
  for i in point:
    r = np.sqrt((i[0]-center[0])**2 + (i[1]-center[1])**2)
    if r <= 0.5:
      pointC.append(i)
  return pointC

# Testing dataset C
dataC = datasetC(1000)
print(dataC)
for i in range(len(dataC)):
  plt.scatter(dataC[i][0], dataC[i][1])
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

def datasetD(n):
  point = datasetC(n)
  pointD = []
  center = np.array((0.5, 0.5))
  for i in point:
    r = np.sqrt((i[0]-center[0])**2 + (i[1]-center[1])**2)
    r = np.round(r, 2)
    if r == 0.50:
      pointD.append(i)
  return pointD


# Testing D 
dataD = datasetD(10000)
print(dataD)
for i in range(len(dataD)):
  plt.scatter(dataD[i][0], dataD[i][1])
plt.gca().set_aspect('equal', adjustable='box')
plt.show()