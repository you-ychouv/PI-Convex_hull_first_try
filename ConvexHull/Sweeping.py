import matplotlib.pyplot as plt
import numpy as np
import time
def isTriClockwise(A, B, C):
  # to test if the triangle is clockwise
    # A = (x,y) is the vertex of the triangle
    AB = [B[0] - A[0], B[1] - A[1]]
    AC = [C[0] - A[0], C[1] - A[1]]
    det = AB[0]* AC[1] - AB[1]* AC[0]
    if det == 0:
        return "this is not a triangle!!!!"
    if det>0:
        return False
    else:
        return True

# test for function isTriClockwise
A = np.array([1,2])
B = np.array([2,1])
C = np.array([3,3])

print(isTriClockwise(A,B,C))
print(isTriClockwise(B,A,C))
print(isTriClockwise(C,B,A))
print(isTriClockwise(B,C,A))

def sweeping(Data):
    # input : list of dataset
    # output : list of connecting points
    # process: sort data, connect two points that won't create concavity

    Data = np.array(Data)
    indices = np.argsort(Data[:,0], kind = 'mergesort')
    Data_sorted = Data[indices].tolist()

    if len(Data_sorted) <= 2:
        return Data_sorted
    upper = []
    for p in Data_sorted:
        while len(upper)>=2 and not isTriClockwise(upper[-2],upper[-1],p):
            upper.pop()
        upper.append(p)
    lower = []
    for p in Data_sorted:
        while len(lower)>=2 and isTriClockwise(lower[-2],lower[-1],p):
            lower.pop()
        lower.append(p)
    convex_hull = upper+list(reversed(lower[1:-1]))
    convex_hull.append(convex_hull[0])

    return convex_hull


# Test the function Sweeping for Upper part
point = np.array([[0,0],[-1,2],[-2,1],[2,4],[4,6]])

t0 = time.time()
d = sweeping(point)
t1 = time.time()
print(f"Total runtime of Sweeping algorithm is {t1 - t0} seconds")

d_arr = np.array(d)
x = d_arr[:,0]
y = d_arr[:,1]

for i in range(len(point)):
    plt.scatter(point[i][0], point[i][1])
plt.plot(x,y)

plt.show()


def plotConvexHull(dataset):
  convex = np.array(sweeping(dataset))

  plt.scatter([p[0] for p in dataset], [p[1] for p in dataset], alpha=0.3)
  plt.plot([p[0] for p in convex], [p[1] for p in convex], 'r-o')

  plt.gca().set_aspect('equal')
  plt.xlabel("coordinate x")
  plt.ylabel("coordinate y")
  plt.title("Convex Hull using Sweeping")
  plt.show()
  return
