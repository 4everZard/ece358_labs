
import math
import random

class Packet(object):
    def __init__(self, packet_type, time, node, N):
        self.type = packet_type
        self.time = time
        self.node = node

class Node(object):
    def __init__(self, node_location, packets):
        print(node_location)
        self.location = node_location
        self.packets = packets
        self.collisions = 0

class Persistant(object):
    def __init__(self):
        self.nodes = []

    def runSimulation(self, N, T, L):
        self.generateNodes(N, T, L)
        L = 1500
        R = 1000000
        S = 0.02/3
        t = 0
        num_transmitted_packets = 0
        top_packets = []
        t_trans = L/R
        for node in self.nodes:
            packet = node.packets.pop(0)
            top_packets.append(packet)
        top_packets.sort(key=lambda x: x.time)
        while t < T and len(top_packets) > 0:
            transmitting_packet = top_packets.pop(0)
            transmitting_node = self.nodes[transmitting_packet.node]
            t = transmitting_packet.time
            collision_occured = False
            for packet in top_packets:
                t_prop = 10*abs(transmitting_packet.node - packet.node)
                if ((transmitting_packet.time + t_prop) < packet.time):
                    #collision
                    collision_occured = True
                    self.nodes[packet.node].collisions += 1

            if (collision_occured):
                transmitting_node.collisions += 1
                num_transmitted_packets += 1

            #update top packets with next in queue from transmitting node
            if (len(transmitting_node.packets) > 0):
                top_packets.append(transmitting_node.packets.pop(0))


    def generateNodes(self, N, T, L):
        for i in range(N):
            packets = self.generatePackets(T, L, i, N)
            packets.sort(key=lambda x: x.time)
            print(packets[0].time)
            node = Node(i, packets)
            self.nodes.append(node)

    def generatePackets(self, time, llama, node, N):
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
            arrival_packet = Packet("Arrival", arrival_time, node, N)
            packets.append(arrival_packet)

            i = arrival_time
        return packets

    def generateVariables(self, llama):
        """
        :param llama: Average number of packets generated/arrived per second
        :return: random number with average value of 1/lambda
        """
        return -(1 / llama) * math.log(1 - random.random())