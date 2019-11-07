from persistent import Persistent
from nonpersistent import NonPersistent


def question1():
    A = [7, 10, 20]
    N = [20, 40, 60, 80, 100]
    for n in N:
        for a in A:
            sim = Persistent()
            sim.runSimulation(n, 1000, a)


def question2():
    A = [7, 10, 20]
    N = [20, 40, 60, 80, 100]
    for n in N:
        for a in A:
            sim = NonPersistent()
            sim.runSimulation(n, 1000, a)


if __name__ == '__main__':
    question1()
    question2()
