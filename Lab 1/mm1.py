import random
import math


class Packet(object):
    def __init__(self, packet_type, time):
        self.type = packet_type
        self.time = time


class SimData(object):
    def __init__(self, idle_counter, rho, EN):
        self.idle = idle_counter
        self.rho = rho
        self.EN = EN


class MM1Simulator(object):
    def __init__(self):
        self.event_scheduler = []
        self.queue_time = 0
        self.num_arrivals = 0
        self.num_departures = 0
        self.num_observers = 0
        self.idle_counter = 0
        self.queue_packets = 0

    def runSimulation(self, llama, T):
        self.generateEvents(T, llama)
        self.generateObservers(T, llama)
        self.event_scheduler.sort(key=lambda x: x.time)
        for event in self.event_scheduler:
            if event.type == "Arrival":
                self.num_arrivals += 1
            elif event.type == "Departure":
                self.num_departures += 1
            elif event.type == "Observer":
                self.num_observers += 1
                if self.num_arrivals == self.num_departures:
                    self.idle_counter += 1
                else:
                    self.queue_packets += self.num_arrivals - self.num_departures

    def generateProcessTime(self, L=2000, C=1000000):
        """
        :param L: average packet size in bits
        :param C: transfer rate in bps
        :return: service time for arrival packet
        """
        bit_length = self.generateVariables(1 / L)
        service_time = bit_length / C

        return service_time

    def generateObservers(self, time, llama):
        """
        :param time: duration of the simulation
        :param llama: average number of events generated/arrived per second
        :return: None
        """
        i = 0
        while i < time:
            observer_time = i + self.generateVariables(5 * llama)
            observer_object = Packet("Observer", observer_time)
            if observer_time > time:
                break
            self.event_scheduler.append(observer_object)

            i = observer_time

    def generateEvents(self, time, llama):
        """
        :param time: duration of the simulation
        :param llama: Average number of packets generated/arrived per second
        :return: None
        """
        i = 0
        while i < time:
            step_time = self.generateVariables(llama)
            arrival_time = i + step_time

            if arrival_time > time:
                break
            arrival_packet = Packet("Arrival", arrival_time)
            self.event_scheduler.append(arrival_packet)

            if self.queue_time > step_time:
                self.queue_time -= step_time
            else:
                self.queue_time = 0

            processing_time = self.generateProcessTime()

            departure_time = arrival_time + self.queue_time + processing_time
            departure_packet = Packet("Departure", departure_time)

            if departure_time < time:
                self.event_scheduler.append(departure_packet)

            self.queue_time += processing_time
            i = arrival_time

    def generateVariables(self, llama):
        """
        :param llama: Average number of packets generated/arrived per second
        :return: random number with average value of 1/lambda
        """
        return -(1 / llama) * math.log(1 - random.random())
