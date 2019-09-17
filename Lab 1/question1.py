import random
import math

L = 75
s = 1000
sum = 0
values = []

for i in range(s):
    U = random.random()
    x = -(1/L) * math.log(1 - U)
    values.append(x)
    print(i, ": ", x)
    sum += x

average = sum/s
print("average: ", average, 1/L)

varianceNum = 0
for value in values:
    varianceNum += (value - average)**2
variance = varianceNum/(s-1)

print("variance: ", variance)
