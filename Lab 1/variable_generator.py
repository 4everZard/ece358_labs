import random
import math


def generateVariables(L, s):
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

    stdev = 0
    for num in values:
        stdev += (num-average)**2

    variance = math.sqrt(stdev/(len(values)-1))

    print("variance: ", variance)
