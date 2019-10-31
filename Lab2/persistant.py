
import math
import random

class Packet(object):
    def __init__(self, packet_type, time):
        self.type = packet_type
        self.time = time
class Node(object):
    def __init__(self, node_id, packets):
        self.id = node_id
        self.packets = packets

class Persistant(object):
    def __init__(self):
        self.nodes = []

    def runSimulation(self, N, T, L):
        print(N, T, L)
        for i in range(N):
            packets = self.generatePackets(T, L)
            node = Node(i, packets)
            self.nodes.append(node)
        for node in self.nodes:
            print(len(node.packets))

    def generatePackets(self, time, llama):
        """
        :param time: duration of the simulation
        :param llama: Average number of packets generated/arrived per second
        :return: None
        """
        packets = []
        i = 0
        while i < time:
            step_time = self.generateVariables(llama)
            arrival_time = i + step_time

            if arrival_time > time:
                break
            arrival_packet = Packet("Arrival", arrival_time)
            packets.append(arrival_packet)

            i = arrival_time
        return packets

    def generateVariables(self, llama):
        """
        :param llama: Average number of packets generated/arrived per second
        :return: random number with average value of 1/lambda
        """
        return -(1 / llama) * math.log(1 - random.random())