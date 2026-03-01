import numpy as np
import random
import matplotlib.pyplot as plt
import Dataset

def MedianofMedian(arr, k): # Returns the k-th smallest element of a given array
    if not 0 <= k < len(arr):
        raise IndexError("k out of bounds")
    if len(arr) == 0:
        raise ValueError("Array is empty.")

    # Small base case: If there is no base case, it could cause overflow
    if len(arr) <= 50:
        return sorted(arr)[k]

    # Split into groups of 5 and compute medians
    groups = [arr[i:i+5] for i in range(0, len(arr), 5)]
    medians = [sorted(g)[len(g)//2] for g in groups]

    # choose a pivot in the list of all medians
    pivot = MedianofMedian(medians, len(medians)//2)

    # Partition around pivot
    left  = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]
    pivs  = [x for x in arr if x == pivot]

    if k < len(left):
        return MedianofMedian(left, k)
    elif k < len(left) + len(pivs):
        return pivot
    else:
       return MedianofMedian(right, k - len(left) - len(pivs))


def median(P): #P is list of point
    n = len(P)
    if n == 0:
        raise ValueError("There is no point in your dataset.")
    k = n // 2
    xs = [p[0] for p in P]
    return MedianofMedian(xs, k)

# Example 
arr = [1,6,7,9,2,3,4,8,10,15,10,19,39,26,9,0]
print(MedianofMedian(arr, 7))

# Linear Programming
def line(p1, p2, x):
    eps = 1e-12
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    if abs(dx) <= eps:
        return float("inf")
    slope = (y2 - y1) / dx
    intercept = y1 - slope * x1
    return slope * x + intercept


def LinearP_upper(points, xm):
    eps = 1e-12

    left  = [p for p in points if p[0] < xm]
    right = [p for p in points if p[0] > xm]
    if not left or not right:
        raise ValueError("Need to have at least one point on both sides of xm.")

    # initial basis: one point on each side
    p1 = random.choice(left)
    p2 = random.choice(right)

    remain = [p for p in points
              if (not np.array_equal(p, p1)) and (not np.array_equal(p, p2))]
    random.shuffle(remain)

    # points already inserted
    P_k = [p1, p2]

    for p in remain:
        # If p is below the current basis
        if p[1] <= line(p1, p2, p[0]):
            P_k.append(p)
            continue

        new_q = None

        # For each q in P_k: we calculate s*(x_q - x_p) >= y_q - y_p accordingly

        if p[0] < xm: # then xm - x_p > 0
            best_s = float("-inf")  
            for q in P_k:
                dx = q[0] - p[0]
                dy = q[1] - p[1]

                if abs(dx) <= eps:
                    if dy > eps:
                        raise RuntimeError("Error due to almost-duplicate x (vertical line).")
                    continue

                # s = (y_q - y_p)/(x_q - x_p)
                slope = dy / dx

                if dx > 0:
                    # s max
                    if slope > best_s:
                        best_s = slope
                        new_q = q
                else:
                    #p on left
                    pass

            p1, p2 = p, new_q

        else:
            # p is on the right of xm then xm - x_p < 0
            best_s = float("inf")

            for q in P_k:
                dx = q[0] - p[0]
                dy = q[1] - p[1]

                if abs(dx) <= eps:
                    if dy > eps:
                        raise RuntimeError("Infeasible due to duplicate x with higher y.")
                    continue

                slope = dy / dx

                if dx < 0:
                    # upper bound: s <= bound
                    if slope < best_s:
                        best_s = slope
                        new_q = q
                else:
                    pass


            # Update basis: ensure p1.x < p2.x
            p1, p2 = new_q, p

        P_k.append(p)

    if p1[0] > p2[0]:
        p1, p2 = p2, p1
# # Just for verify, 
#     for p in points:
#         if p[1] > line(p1, p2, p[0]) + eps:
#             raise RuntimeError("Line is not above all points.")

    return p1, p2



# Linear Programming code for the lower hull; symmetric. 
def LinearP_lower(points, xm):
    # flip y since it is symmetric
    points2 = [(p[0], -p[1]) for p in points]

    q1, q2 = LinearP_upper(points2, xm)

    p1 = (q1[0], -q1[1])
    p2 = (q2[0], -q2[1])

    if p1[0] > p2[0]:
        p1, p2 = p2, p1

    return p1, p2


def UpperconvexHull(points):
    if len(points) <= 1:
        return points
    if len(points) == 2:
        a, b = points[0], points[1]
        return [a, b] if a[0] <= b[0] else [b, a]

    xm = median(points)
    p1, p2 = LinearP_upper(points, xm)

    if p1[0] > p2[0]:
        p1, p2 = p2, p1

    # Subproblems
    left_pts  = [p for p in points if p[0] < p1[0]] + [p1]
    right_pts = [p for p in points if p[0] > p2[0]] + [p2]

    left_hull  = UpperconvexHull(left_pts)  if len(left_pts)  > 1 else [p1]
    right_hull = UpperconvexHull(right_pts) if len(right_pts) > 1 else [p2]

    # Remove duplicated basis points
    if left_hull and np.array_equal(left_hull[-1], p1):
        left_hull = left_hull[:-1]
    if right_hull and np.array_equal(right_hull[0], p2):
        right_hull = right_hull[1:]

    return left_hull + [p1, p2] + right_hull


def LowerconvexHull(points):
    if len(points) <= 1:
        return points
    if len(points) == 2:
        a, b = points[0], points[1]
        return [a, b] if a[0] <= b[0] else [b, a]

    xm = median(points)
    p1, p2 = LinearP_lower(points, xm)

    if p1[0] > p2[0]:
        p1, p2 = p2, p1

    left_pts  = [p for p in points if p[0] < p1[0]] + [p1]
    right_pts = [p for p in points if p[0] > p2[0]] + [p2]

    left_hull  = LowerconvexHull(left_pts)  if len(left_pts)  > 1 else [p1]
    right_hull = LowerconvexHull(right_pts) if len(right_pts) > 1 else [p2]

    if left_hull and np.array_equal(left_hull[-1], p1):
        left_hull = left_hull[:-1]
    if right_hull and np.array_equal(right_hull[0], p2):
        right_hull = right_hull[1:]

    return left_hull + [p1, p2] + right_hull


def convexHull(point):
    upper = UpperconvexHull(point)
    lower = LowerconvexHull(point)

    # upper goes left to right
    # lower goes left to right
    # Combine: upper + reversed(lower excluding endpoint)

    hull = upper + list(reversed(lower[0:-1]))

    return hull

# Testing with dataset B 
datasetB = Dataset.datasetB(100)
datasetC = Dataset.datasetC(1000)

def plotConvexLP(point): 
    g = convexHull(point)
    plt.scatter([p[0] for p in point], [p[1] for p in point], alpha=0.3)
    plt.plot([p[0] for p in g], [p[1] for p in g], 'r-o')
    plt.gca().set_aspect('equal')
    plt.xlabel("coordinate x")
    plt.ylabel("coordinate y")
    plt.title("Convex Hull using Output sensitive algorithm ")
    plt.show()
    return 

plotConvexLP(datasetB)
plotConvexLP(datasetC)