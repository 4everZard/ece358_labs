import math
import random


class Packet(object):
    def __init__(self, packet_type, time, node, N):
        self.type = packet_type
        self.time = time
        self.node = node


class Node(object):
    def __init__(self, node_location, packets):
        self.location = node_location
        self.packets = packets
        self.collisions = 0

    def getBackoff(self):
        R = random.random() * ((2 ** self.collisions) - 1)
        backoff = R * (1 / 1000000)
        return backoff


class Persistant(object):
    def __init__(self):
        self.nodes = []

    def runSimulation(self, N, T, A):
        self.generateNodes(N, T, A)
        L = 1500
        R = 1000000
        S = (2 / 3) * 3 * 10 ** 8
        t = 0
        num_transmitted_packets = 0
        num_successful_packets = 0
        num_dropped_packets = 0
        top_packets = []
        t_trans = L / R
        for node in self.nodes:
            packet = node.packets.pop(0)
            top_packets.append(packet)

        while len(top_packets) > 0 and t < T:
            top_packets.sort(key=lambda x: x.time)
            transmitting_packet = top_packets[0]
            if transmitting_packet.time == T:
                break

            transmitting_node = self.nodes[transmitting_packet.node]
            t = transmitting_packet.time

            collision_occured_i = False
            collision_occured_j = False
            t_prop = 0

            top_packets.sort(key=lambda x: x.node)
            i = transmitting_packet.node + 1
            j = transmitting_packet.node - 1
            collision_occured = False

            while i < len(top_packets) or j >= 0:


                if i < len(top_packets):
                    if top_packets[i].time < T:
                        # Still have packets to visit on the right side
                        t_prop = 10 * abs(transmitting_packet.node - i) / S
                        if (transmitting_packet.time + t_prop) > top_packets[i].time:
                            collision_occured_i = True
                if j >= 0:
                    if top_packets[j].time < T:
                        # Still have packets to visit on the left side
                        t_prop = 10 * abs(transmitting_packet.node - j) / S
                        if (transmitting_packet.time + t_prop) > top_packets[j].time:
                            collision_occured_j = True

                if collision_occured_i and collision_occured_j:
                    collision_occured = True
                    # Both sides collided, take the first collision
                    first_collision_time = min(top_packets[i].time, top_packets[j].time)
                    if first_collision_time == top_packets[i].time:
                        colliding_node = self.nodes[top_packets[i].node]
                        collision_index = i
                        colliding_packet = top_packets[i]
                    else:
                        colliding_node = self.nodes[top_packets[j].node]
                        collision_index = j
                        colliding_packet = top_packets[j]

                    colliding_node.collisions += 1
                    if colliding_node.collisions > 10:
                        # drop packet
                        num_dropped_packets += 1
                        colliding_node.collisions = 0
                        top_packets.pop(collision_index)
                        if len(colliding_node.packets) > 0:
                            newPacket = colliding_node.packets.pop(0)
                            if newPacket.time < t:
                                newPacket.time = t
                            top_packets.append(newPacket)
                        else:
                            top_packets.append(Packet(packet_type=None, time=T, node=colliding_packet.node, N=N))

                    else:
                        colliding_packet.time += colliding_node.getBackoff()

                    break

                elif collision_occured_i and not collision_occured_j:
                    # Collision found on the right side
                    collision_occured = True
                    colliding_node = self.nodes[top_packets[i].node]
                    collision_index = i
                    colliding_packet = top_packets[i]

                    colliding_node.collisions += 1
                    if colliding_node.collisions > 10:
                        # drop packet
                        num_dropped_packets += 1
                        colliding_node.collisions = 0
                        top_packets.pop(collision_index)
                        if len(colliding_node.packets) > 0:
                            newPacket = colliding_node.packets.pop(0)
                            if newPacket.time < t:
                                newPacket.time = t
                            top_packets.append(newPacket)
                        else:
                            top_packets.append(Packet(packet_type=None, time=T, node=colliding_packet.node, N=N))
                    else:
                        colliding_packet.time += colliding_node.getBackoff()

                    break

                elif collision_occured_j and not collision_occured_i:
                    # Collision found on the left side
                    collision_occured = True
                    colliding_node = self.nodes[top_packets[j].node]
                    collision_index = j
                    colliding_packet = top_packets[j]

                    colliding_node.collisions += 1
                    if colliding_node.collisions > 10:
                        # drop packet
                        num_dropped_packets += 1
                        colliding_node.collisions = 0
                        top_packets.pop(collision_index)
                        if len(colliding_node.packets) > 0:
                            newPacket = colliding_node.packets.pop(0)
                            if newPacket.time < t:
                                newPacket.time = t
                            top_packets.append(newPacket)
                        else:
                            top_packets.append(Packet(packet_type=None, time=T, node=colliding_packet.node, N=N))
                    else:
                        colliding_packet.time += colliding_node.getBackoff()

                    break

                i += 1
                j -= 1

            # update transmitting node after collision
            if collision_occured:
                num_transmitted_packets += 2
                transmitting_node.collisions += 1
                if colliding_node.collisions > 10:
                    # drop packet
                    num_dropped_packets += 1
                    transmitting_node.collisions = 0
                    top_packets.pop(transmitting_node.location)
                    if len(transmitting_node.packets) > 0:
                        newPacket = transmitting_node.packets.pop(0)
                        if newPacket.time < t:
                            newPacket.time = t
                        top_packets.append(newPacket)
                    else:
                        top_packets.append(Packet(packet_type=None, time=T, node=transmitting_node.location, N=N))

                else:
                    # readd to top nodes as failed transmission
                    transmitting_packet.time += transmitting_node.getBackoff()
            else:
                # successful send
                num_transmitted_packets += 1
                num_successful_packets += 1
                transmitting_node.collisions = 0
                top_packets.pop(transmitting_node.location)
                if len(transmitting_node.packets) > 0:
                    top_packets.append(transmitting_node.packets.pop(0))
                else:
                    top_packets.append(Packet(packet_type=None, time=T, node=transmitting_node.location, N=N))
                for packet in top_packets:
                    busy_time = transmitting_packet.time + t_trans + 10 * abs(
                        transmitting_packet.node - packet.node) / S
                    if packet.time < busy_time:
                        packet.time = busy_time

                t += t_trans

            
        print("N: ", N, " A: ", A)
        print(num_transmitted_packets)
        print(num_successful_packets)
        print(num_dropped_packets)

    def generateNodes(self, N, T, L):
        # A = [Packet("A", 0.21, 0, 4), Packet("A", 0.26, 0, 4), Packet("A", 0.29, 0, 4), Packet("A", 0.31, 0, 4)]
        # B = [Packet("A", 0.09, 1, 4), Packet("A", 0.1, 1, 4), Packet("A", 0.15, 1, 4), Packet("A", 0.19, 1, 4)]
        # C = [Packet("A", 0.13, 2, 4), Packet("A", 0.16, 2, 4), Packet("A", 0.18, 2, 4), Packet("A", 0.22, 2, 4)]
        # D = [Packet("A", 0.23, 3, 4), Packet("A", 0.27, 3, 4), Packet("A", 0.30, 3, 4), Packet("A", 0.33, 3, 4)]
        # self.nodes = [Node(0, A), Node(1, B), Node(2, C), Node(3, D)]
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
