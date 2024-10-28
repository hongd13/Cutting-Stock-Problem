import numpy as np
import random
import matplotlib.pyplot as plt
from random_search import RandomSearch
from aco import ACO
from evo import EVO


class Cutting_Problem():
    def __init__(self, case, seed=None):
        """
        Initiate a Cutting_Problem instance.

        :param case: array of stock lengths
        :param c: array of stock costs
        :param seed: random seed
        :return: None
        """
        self.rng = random
        if seed is not None:
            self.rng.seed(seed)  # setting seed

        self.stocks = dict(zip(case["l"], case["c"]))
        self.orders = dict(zip(case["rl"], case["q"]))

        self.rs = RandomSearch(self.stocks, self.rng)
        self.evo = EVO(self.stocks, self.rng, self.rs)
        self.aco = ACO(self.stocks, self.rng, self.rs, self.evo)
        self.pipe = [self.rs, self.evo, self.aco]

        for x in self.pipe:
            x.set_order(self.orders)

    def set_order(self, rl, q):
        """
        Set order

        :param rl: array of requested lengths
        :param q: array of requested quantities
        :return: None
        """
        self.orders = dict(zip(rl, q))
        for x in self.pipe:
            x.set_order(self.orders)

    def random_search(self, iterations=100, t=4, target=0, population=100):
        best, fitness, time, log = self.rs.run(iterations=iterations, t=t, target=target, population=population)
        print("Best solution: ", best)
        print("Fitness: ", fitness)
        print("Time elapsed: {}s".format(time))
        self.plot_log(log)

    def evo_alg(self, pop=None, population=500, iterations=500, t=600, target=0, m=5, mutation_strength=0.5):
        best, fitness, time, log = self.evo.run(pop=pop, population=population, iterations=iterations, t=t, target=target, m=m, mutation_strength=mutation_strength)
        print("Best solution: ", best)
        print("Fitness: ", fitness)
        print("Time elapsed: {}s".format(time))
        self.plot_log(log)

    def aco_alg(self, pop=None, population=500, cycles=500, decay=-0.5):
        best, fitness, time, log = self.aco.run(pop=pop, population=population, cycles=cycles, decay=decay)
        print("Best solution: ", best)
        print("Fitness: ", fitness)
        print("Time elapsed: {}s".format(time))
        self.plot_log(log)

    def iter_aco_alg(self, pop=None, population=500, cycles=500, decay=-0.5, iterations=100):
        best, fitness, time, log = self.aco.run(pop=pop, population=population, cycles=cycles, decay=decay)
        for j in range(iterations):
            print("------------Iteration {}------------".format(j))
            pop = [best]
            for j in range(population - 1):
                pop.append(self.rs.random_candidate())
            best, fitness, new_time, new_log = self.aco.run(pop=pop, population=population, cycles=cycles, decay=decay)
            log["candidates"] = log["candidates"] + new_log["candidates"]
            old_time = log["times"][-1]
            del log["times"][-1]
            del log["candidates"][-1]
            new_log["times"] = [old_time + new_log_time for new_log_time in new_log["times"]]
            log["times"] = log["times"] + new_log["times"]
        print("Best solution: ", best)
        print("Fitness: ", fitness)
        print("Time elapsed: {}s".format(time))
        self.plot_log(log)

    def evo_aco(self):
        best_pops = []
        log = {"candidates": [], "times": []}
        for i in range(10):
            best, fitness, time, new_log = self.evo.run()
            best_pops.append(best)
            log["candidates"].append(new_log["candidates"][-1])
            log["times"].append(new_log["times"][-1])
        best, fitness, time, new_log = self.aco.run(pop=best_pops, population=10)
        log["candidates"].append(new_log["candidates"][-1])
        log["times"].append(new_log["times"][-1])
        for i, time in enumerate(log["times"]):
            if i > 0:
                log["times"][i] += log["times"][i - 1]
        print("Best solution: ", best)
        print("Fitness: ", fitness)
        print("Time elapsed: {}s".format(time))
        self.plot_log(log)

    def plot_log(self, log):
        fitness = [self.rs.get_fitness(c) for c in log["candidates"]]
        times = log["times"]

        plt.plot(times, fitness, marker='o', linestyle='-')
        plt.xlabel("Time (s)")
        plt.ylabel("Fitness")
        plt.title("Performance Log")
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    """
    Setting test cases, initiate a cutting problem instance, invoke algorithm and set parameters.
    """

    case1 = {
        "l": [10, 13, 15],  # stock lengths
        "c": [100, 130, 150],  # stock costs
        "rl": [3, 4, 5, 6, 7, 8, 9, 10],  # requested lengths
        "q": [5, 2, 1, 2, 4, 2, 1, 3]  # requested quantities
    }
    case2 = {
        "l": [50, 80, 100],  # stock lengths
        "c": [100, 175, 250],  # stock costs
        "rl": [20, 25, 30],  # requested lengths
        "q": [2, 2, 4]  # requested quantities
    }
    case3 = {
        "l": [4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500],  # stock lengths
        "c": [86, 85, 83, 79, 68, 66, 64, 63],  # stock costs
        "rl": [2350, 2250, 2200, 2100, 2050, 2000, 1950, 1900, 1850, 1700, 1650, 1350, 1300, 1250, 1200, 1150, 1100,
               1050],  # requested lengths
        "q": [2, 4, 4, 15, 6, 11, 6, 15, 13, 5, 2, 9, 3, 6, 10, 4, 8, 3]  # requested quantities
    }
    case4 = {
        "l": [120, 115, 110, 105, 100],  # stock lengths
        "c": [12, 11.5, 11, 10.5, 10],  # stock costs
        "rl": [21, 22, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
               55, 56, 57, 59, 60, 61, 63, 65, 66, 67],  # requested lengths
        "q": [13, 15, 7, 5, 9, 9, 3, 15, 18, 17, 4, 17, 20, 9, 4, 19, 4, 12, 15, 3, 20, 14, 15, 6, 4, 7, 5, 19, 19, 6,
              3, 7, 20, 5, 10, 17]  # requested quantities
    }
    case5 = {
        "l": [],  # stock lengths
        "c": [],  # stock costs
        "rl": [],  # requested lengths
        "q": []  # requested quantities
    }
    cp = Cutting_Problem(case3, seed=42)

    # initiating a testing population
    test_pop = []
    for i in range(500):
        test_pop.append(cp.rs.random_candidate())

    # plotting testing population fitness distribution
    cp.rs.plot_gaussian()

    # choose algorithms here
    alg = "evo"  # rs, evo, aco

    if alg == "rs":
        """
        Random Search Algorithm
        """
        cp.random_search(iterations=100, population=100)
    elif alg == "evo":
        """
        Evolutionary Algorithm
        """
        cp.evo_alg(pop=test_pop, population=500, iterations=500, t=600, target=0, m=5, mutation_strength=0.5)
    elif alg == "aco":
        """
        Ant Colony Optimization Algorithm
        """
        cp.aco_alg(pop=test_pop, population=500, cycles=500, decay=-0.5)