import random
import math

#For a FIFO, we will use a python list.
#ie:
#x = []
#x.append(3) <- enqueue
#x.pop(0) <- dequeue

class Packet(object):
    def __init__(self, type, time):
        self.type = type
        self.time = time

class Simulator(object):

    def __init__(self):
        self.event_scheduler = []
        self.


    def runSimulation(self):

        pass

    def generateProcessTime(self):
        L = 2000
        C = 8000000
        bit_length = self.generateVariables(1/L)

        return bit_length/C

    def generateObservers(self, time):
        i = 0
        while i < time:
            observer_time = i + self.generateVariables(llama=5*75)
            observer_object = Packet("Observer", observer_time)
            if observer_time > time:
                break
            self.event_scheduler.append(observer_object)

            i = observer_time

    def generateEvents(self, time):
        i = 0
        while i < time:
            arrival_time = i + self.generateVariables(llama=75)

            if arrival_time > time:
                break
            arrival_packet = Packet("Arrival", arrival_time)
            self.event_scheduler.append(arrival_packet)

            processing_time = self.generateProcessTime()

            departure_time = arrival_time + processing_time
            departure_packet = Packet("Departure", departure_time)

            if departure_time < time:
                self.event_scheduler.append(departure_packet)

            i = arrival_time


    def generateVariables(self, llama):
        return -(1 / llama) * math.log(1 - random.random())

if __name__ == "__main__":
    sim = Simulator()
    sim.generateEvents(10)
    sim.generateObservers(10)
    sim.event_scheduler.sort(key=lambda x: x.time)

    sim.runSimulation()

    print(len(sim.event_scheduler))
    for event in sim.event_scheduler:
        print(event.type, event.time)
