from persistant import Persistant

def question1():
    A = [7, 10, 20]
    N = [20, 40, 60, 80, 100]
    for n in N:
        for a in A:
            sim = Persistant()
            sim.runSimulation(n, 2000, a)

if __name__ == '__main__':
    question1()