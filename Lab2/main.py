from persistant import Persistant

def question1():
    A = 7
    N = 20
    sim = Persistant()
    sim.runSimulation(N, 100, A)

if __name__ == '__main__':
    question1()