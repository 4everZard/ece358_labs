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


class Persistent(object):
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

        while t < T:
            top_packets.sort(key=lambda x: x.time)
            transmitting_packet = top_packets[0]
            if transmitting_packet.time == T:
                break

            transmitting_node = self.nodes[transmitting_packet.node]
            t = transmitting_packet.time

            collision_occurred_i = False
            collision_occurred_j = False

            top_packets.sort(key=lambda x: x.node)
            i = transmitting_packet.node + 1
            j = transmitting_packet.node - 1
            collision_occurred = False
            colliding_node = None

            while i < len(top_packets) or j >= 0:

                if i < len(top_packets):
                    if top_packets[i].time < T:
                        # Still have packets to visit on the right side
                        t_prop = 10 * abs(transmitting_packet.node - i) / S
                        if (transmitting_packet.time + t_prop) > top_packets[i].time:
                            collision_occurred_i = True
                if j >= 0:
                    if top_packets[j].time < T:
                        # Still have packets to visit on the left side
                        t_prop = 10 * abs(transmitting_packet.node - j) / S
                        if (transmitting_packet.time + t_prop) > top_packets[j].time:
                            collision_occurred_j = True

                if collision_occurred_i and collision_occurred_j:
                    collision_occurred = True
                    # Both sides collided, take the first collision
                    first_collision_time = min(top_packets[i].time, top_packets[j].time)
                    if first_collision_time == top_packets[i].time:
                        collision_index = i
                    else:
                        collision_index = j

                    self.nodes[top_packets[collision_index].node].collisions += 1
                    if self.nodes[top_packets[collision_index].node].collisions > 10:
                        # drop packet
                        num_dropped_packets += 1
                        self.nodes[top_packets[collision_index].node].collisions = 0
                        if len(self.nodes[top_packets[collision_index].node].packets) > 0:
                            newPacket = self.nodes[top_packets[collision_index].node].packets.pop(0)
                            if newPacket.time < t:
                                newPacket.time = t
                            top_packets.pop(collision_index)
                            top_packets.append(newPacket)
                        else:
                            top_packets.pop(collision_index)
                            top_packets.append(Packet(packet_type=None, time=T, node=top_packets[collision_index].node, N=N))

                    else:
                        top_packets[collision_index].time += self.nodes[top_packets[collision_index].node].getBackoff()
                    break

                elif collision_occurred_i and not collision_occurred_j:
                    # Collision found on the right side
                    collision_occurred = True
                    collision_index = i

                    self.nodes[top_packets[i].node].collisions += 1
                    if self.nodes[top_packets[i].node].collisions > 10:
                        # drop packet
                        num_dropped_packets += 1
                        self.nodes[top_packets[i].node].collisions = 0

                        if len(self.nodes[top_packets[i].node].packets) > 0:
                            newPacket = self.nodes[top_packets[i].node].packets.pop(0)
                            if newPacket.time < t:
                                newPacket.time = t
                            top_packets.pop(collision_index)
                            top_packets.append(newPacket)
                        else:
                            top_packets.pop(collision_index)
                            top_packets.append(Packet(packet_type=None, time=T, node=top_packets[i].node, N=N))
                    else:
                        top_packets[i].time += self.nodes[top_packets[i].node].getBackoff()
                    break

                elif collision_occurred_j and not collision_occurred_i:
                    # Collision found on the left side
                    collision_occurred = True
                    collision_index = j

                    self.nodes[top_packets[j].node].collisions += 1
                    if self.nodes[top_packets[j].node].collisions > 10:
                        # drop packet
                        num_dropped_packets += 1
                        self.nodes[top_packets[j].node].collisions = 0
                        if len(self.nodes[top_packets[j].node].packets) > 0:
                            newPacket = self.nodes[top_packets[j].node].packets.pop(0)
                            if newPacket.time < t:
                                newPacket.time = t
                            top_packets.pop(collision_index)
                            top_packets.append(newPacket)
                        else:
                            top_packets.pop(collision_index)
                            top_packets.append(Packet(packet_type=None, time=T, node=top_packets[j].node, N=N))
                    else:
                        top_packets[j].time += self.nodes[top_packets[j].node].getBackoff()
                    break

                i += 1
                j -= 1

            # update transmitting node after collision
            if collision_occurred:
                num_transmitted_packets += 2
                transmitting_node.collisions += 1
                if transmitting_node.collisions > 10:
                    # drop packet
                    num_dropped_packets += 1
                    transmitting_node.collisions = 0
                    if len(transmitting_node.packets) > 0:
                        newPacket = transmitting_node.packets.pop(0)
                        if newPacket.time < t:
                            newPacket.time = t
                        top_packets.pop(transmitting_node.location)
                        top_packets.append(newPacket)
                    else:
                        top_packets.pop(transmitting_node.location)
                        top_packets.append(Packet(packet_type=None, time=T, node=transmitting_node.location, N=N))

                else:
                    # read to top nodes as failed transmission
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
        print("Total:", num_transmitted_packets)
        print("Success:", num_successful_packets)
        print("Efficiency:", num_successful_packets / num_transmitted_packets)

    def generateNodes(self, N, T, L):
        for i in range(N):
            packets = self.generatePackets(T, L, i, N)
            packets.sort(key=lambda x: x.time)
            node = Node(i, packets)
            self.nodes.append(node)

    def generatePackets(self, time, llama, node, N):
        """
        :param N: Number of Nodes
        :param node: Node index
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
