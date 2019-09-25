from variable_generator import generateVariables
from mm1 import MM1Simulator, SimData
from mm1k import MM1KSimulator, SimData_mm1k


def question1():
    generateVariables(L=75, s=1000)


def question3():
    rho = 0.25
    simulators = []
    while rho <= 0.95:
        llama = rho * (1000000/2000)
        sim = MM1Simulator()
        sim.runSimulation(llama, T=1000)
        EN = sim.queue_packets/sim.num_observers
        print(rho)
        data = SimData(sim.idle_counter/sim.num_observers, rho, EN)
        simulators.append(data)
        rho = round(rho + 0.1, 2)

    for simulator in simulators:
        print(simulator.rho, simulator.EN, simulator.idle)


def question4():
    rho = 1.2
    llama = rho * (1000000/2000)
    sim = MM1Simulator()
    sim.runSimulation(llama, T=1000)
    EN = sim.queue_packets/sim.num_observers
    print(rho)
    print(sim.idle_counter / sim.num_observers, rho, EN)


def question5():
    rho = 0.95
    llama = rho * (1000000 / 2000)
    sim = MM1KSimulator()
    sim.runSimulation(llama, T=1000, K=10)
    EN = sim.queue_packets / sim.num_observers
    print(rho)
    print(sim.idle_counter / sim.num_observers, rho, EN)

def question6():
    rho = 0.5
    k_values = [10, 25, 50]
    simulators = []
    while rho <= 1.5:
        for k in k_values:
            llama = rho * (1000000 / 2000)
            sim = MM1KSimulator()
            sim.runSimulation(llama, T=1000, K=k)
            EN = sim.queue_packets / sim.num_observers
            loss = sim.dropped_packets/sim.total_packets_generated
            idle = sim.idle_counter/sim.num_observers
            data = SimData_mm1k(rho, k, EN, idle, loss)
            simulators.append(data)
        rho = round(rho + 0.1, 2)

    for simulator in simulators:
        print(simulator.rho, ",", simulator.K, ",", simulator.EN, ",", simulator.idle, ",", simulator.loss)





if __name__ == '__main__':
    #question1()
    #question3()
    #question4()
    #question5()
    question6()

