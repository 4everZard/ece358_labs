
import math
import random

class Packet(object):
    def __init__(self, packet_type, time, node, N):
        self.type = packet_type
        self.time = time
        self.node = node
        self.dropped = False

class Node(object):
    def __init__(self, node_location, packets):
        self.location = node_location
        self.packets = packets
        self.collisions = 0

    def getBackoff(self):
        R = random.random()*((2**self.collisions) - 1)
        backoff = R * (1/1000000)
        return backoff

class Persistant(object):
    def __init__(self):
        self.nodes = []

    def runSimulation(self, N, T, L):
        self.generateNodes(N, T, L)
        L = 1500
        R = 1000000
        S = (2/3) * 3 * 10**8
        t = 0
        num_transmitted_packets = 0
        num_successful_packets = 0
        top_packets = []
        t_trans = L/R
        for node in self.nodes:
            packet = node.packets.pop(0)
            top_packets.append(packet)

        while len(top_packets) > 0:
            top_packets.sort(key=lambda x: x.time)
            transmitting_packet = top_packets.pop(0)
            transmitting_node = self.nodes[transmitting_packet.node]
            collision_occured = False
            for i, packet in enumerate(top_packets):
                t_prop = 10*abs(transmitting_packet.node - packet.node)/S
                if ((transmitting_packet.time + t_prop) < packet.time):
                    #collision
                    collision_occured = True
                    colliding_node = self.nodes[packet.node]
                    colliding_node.collisions += 1
                    if (colliding_node.collisions > 10):
                        #drop packet
                        packet.dropped = True
                        colliding_node.collisions = 0
                        top_packets.pop(i)
                        if (len(self.nodes[packet.node].packets) > 0):
                            top_packets.append(self.nodes[packet.node].packets.pop(0))
                    else:
                        packet.time += colliding_node.getBackoff()

            #update transmitting node after collision
            if (collision_occured):
                transmitting_node.collisions += 1
                if (colliding_node.collisions > 10):
                    #drop packet
                    transmitting_packet.dropped = True
                    transmitting_node.collisions = 0
                    if (len(transmitting_node.packets) > 0):
                        top_packets.append(transmitting_node.packets.pop(0))
                else:
                    #readd to top nodes as failed transmission
                    transmitting_packet.time += transmitting_node.getBackoff()
                    top_packets.append(transmitting_packet)
            else:
                #successful send
                print(transmitting_packet.node)
                num_successful_packets += 1
                transmitting_node.collisions = 0
                if len(transmitting_node.packets) > 0:
                    top_packets.append(transmitting_node.packets.pop(0))
                for packet in top_packets:
                    busy_time = transmitting_packet.time + t_trans + 10*abs(transmitting_packet.node - packet.node)/S
                    if (packet.time < busy_time):
                        packet.time = busy_time

                t = transmitting_packet.time + t_trans

            num_transmitted_packets += 1
        print(num_transmitted_packets)
        print(num_successful_packets)

    def generateNodes(self, N, T, L):
        for i in range(N):
            packets = self.generatePackets(T, L, i, N)
            packets.sort(key=lambda x: x.time)
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