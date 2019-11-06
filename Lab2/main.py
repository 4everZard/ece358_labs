from persistent import Persistent


def question1():
    A = [12]
    N = [20, 40, 60, 80, 100]
    for n in N:
        for a in A:
            sim = Persistent()
            sim.runSimulation(n, 1000, a)


if __name__ == '__main__':
    question1()
