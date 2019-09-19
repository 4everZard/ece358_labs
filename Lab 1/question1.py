import random
import math

#For a FIFO, we will use a python list.
#ie:
#x = []
#x.append(3) <- enqueue
#x.pop(0) <- dequeue

class Simulator(object):

    def __init__(self):
        pass

    def generateVariables(self,):
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

if __name__ == "__main__":
    sim = Simulator()
    sim.generateVariables()