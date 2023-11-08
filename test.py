import numpy as np
import timeit


x = np.array([20, 30, 60, 25, 80])
y = np.array([10, 23, 12, 12, 15])
z = [0, 0, 0, 0, 0]

test = np.array(np.ones(3))*30

def sub(x,y,z):
    for index, item in enumerate(x):
        if abs(x[index] - y[index]) > 30:
            z[index] = x[index]
    print(z)

def sub_fast(x,z):
    x = x - 30
    for i in range(len(x)):
        if x[i] > 0:
            z[i] = x[i]
    print(z)


n=3
result = timeit.timeit(stmt='sub(x,y,z)', globals=globals(), number=n)
print(f"Execution time is {result / n} seconds")

result = timeit.timeit(stmt='sub_fast(x,z)', globals=globals(), number=n)
print(f"Execution time is {result / n} seconds")