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

class SimData(object):
    def __init__(self, idle_counter, rho, EN):
        self.idle = idle_counter
        self.rho = rho
        self.EN = EN

class Simulator(object):

    def __init__(self):
        self.event_scheduler = []
        self.queueTime = 0
        self.num_arrivals = 0
        self.num_departures = 0
        self.num_observers = 0
        self.idle_counter = 0
        self.queue_packets = 0

    def runSimulation(self, llama,T):
        self.generateEvents(T, llama)
        self.generateObservers(T, llama)
        self.event_scheduler.sort(key=lambda x: x.time)
        #print(len(self.event_scheduler))
        for event in self.event_scheduler:
            if (event.type == "Arrival"):
                self.num_arrivals += 1
            elif (event.type == "Departure"):
                self.num_departures += 1
            elif (event.type == "Observer"):
                self.num_observers += 1
                if (self.num_arrivals == self.num_departures):
                    self.idle_counter += 1
                else:
                    self.queue_packets += self.num_arrivals - self.num_departures
            #print(event.type, event.time)
        # print(self.num_arrivals, self.num_departures, self.num_observers, self.idle_counter)

    def generateProcessTime(self):
        L = 2000
        C = 1000000
        bit_length = self.generateVariables(1/L)

        return bit_length/C

    def generateObservers(self, time, llama):
        i = 0
        while i < time:
            observer_time = i + self.generateVariables(5*llama)
            observer_object = Packet("Observer", observer_time)
            if observer_time > time:
                break
            self.event_scheduler.append(observer_object)

            i = observer_time

    def generateEvents(self, time, llama):
        i = 0
        while i < time:
            stepTime = self.generateVariables(llama)
            arrival_time = i + stepTime

            if arrival_time > time:
                break
            arrival_packet = Packet("Arrival", arrival_time)
            self.event_scheduler.append(arrival_packet)

            if self.queueTime > stepTime:
                self.queueTime -= stepTime
            else:
                self.queueTime = 0
            
            processing_time = self.generateProcessTime()

            departure_time = arrival_time + self.queueTime + processing_time
            departure_packet = Packet("Departure", departure_time)

            if departure_time < time:
                self.event_scheduler.append(departure_packet)

            self.queueTime += processing_time
            i = arrival_time


    def generateVariables(self, llama):
        return -(1 / llama) * math.log(1 - random.random())

if __name__ == "__main__":
    rho = 0.25
    simulators = []
    while rho <= 0.95:
        llama = rho * (1000000/2000)
        sim = Simulator()
        sim.runSimulation(llama, 1000)
        EN = sim.queue_packets/1000
        print(rho)
        data = SimData(sim.idle_counter/1000, rho, EN)
        simulators.append(data)
        rho = round(rho + 0.1, 2)

    for simulator in simulators:
        print(simulator.rho, simulator.EN, simulator.idle)
