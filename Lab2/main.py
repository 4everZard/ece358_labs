from persistant import Persistant

def question1():
    rho = 0.25
    llama = rho * (1000000 / 2000)
    sim = Persistant()
    sim.runSimulation(15, 1000, llama)

if __name__ == '__main__':
    question1()