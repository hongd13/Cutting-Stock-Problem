import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class RandomSearch:
    def __init__(self, stocks, rng):
        """
        :param stocks: dictionary of stocks
        :param rng: random number generator

        :return:
        """
        self.rng = rng
        self.stocks = stocks
        self.orders = {}

    def run(self, iterations=100, t=4, target=0, population=100):
        """
        Runs the random search over the given number of iterations,
        or time,
        or until target is reached.

        :param iterations: number of iterations
        :param t: time
        :param target: solution fitness target
        :param population: number of population

        :return: the best solution, fitness, time elapsed (in seconds)
        """
        log = {"candidates": [],
               "times": []}
        print("----Random Search----")
        start_time = time.time()
        go = True
        best = []  # best candidate
        while go:
            for i in range(iterations):
                print("Iteration {}".format(i))
                pop = []  # array of candidates
                for j in range(population):
                    pop.append(self.random_candidate())
                best, log = self.get_best(best, pop, log=log, start_time=start_time)
                if self.get_fitness(best) <= target:
                    go = False
                    print("Target reached! Terminating.")
                    return best, self.get_fitness(best), time.time() - start_time  # target hit, terminate early
            go = False
        print("Search cycle finished. Terminating.")
        return best, self.get_fitness(best), time.time() - start_time, log

    def set_order(self, orders):
        """
        Set order

        :param orders: dictionary of orders

        :return:
        """
        self.orders = orders

    def random_candidate(self, orders=None, candidate=None):
        """
        Generates a random candidate and returns it.

        :param orders: dictionary of orders
        :param candidate: existing candidate

        :return: candidate
        """
        if orders is None:
            orders = self.orders.copy()
        if candidate is None:
            candidate = []  # array of activities
        while sum(orders.values()) > 0:  # while there are orders remaining
            # array of used stock length and covered orders, {l, {rl...}}
            a = [self.rng.choice(list(self.stocks.keys()))]
            fittable_orders = self._get_fittable_orders(a, orders)
            while fittable_orders:  # while more orders can fit into this activity
                order = self.rng.choice(fittable_orders)
                a.append(order)
                orders[order] -= 1
                fittable_orders = self._get_fittable_orders(a, orders)
            candidate.append(a)
        return candidate

    def get_fitness(self, candidate):
        """
        Calculates the fitness of the candidate (total cost), lower the better.

        :param candidate: array of activities

        :return: integer of the fitness
        """
        cost = 0
        for a in candidate:
            cost += self.stocks[a[0]]
        return cost

    def get_best(self, best, pop, log=None, start_time=None):
        """
        Return the best candidate within the population.

        :param best: current best candidate
        :param pop: population

        :return: the best candidate (lowest cost)
        """
        for c in pop:
            if len(best) == 0 or self.get_fitness(c) < self.get_fitness(best):
                best = c
                if log is not None:
                    log["candidates"].append(best)
                    log["times"].append(time.time() - start_time)
        if log is not None:
            return best, log
        return best

    def _get_fittable_orders(self, a, orders):
        """
        Return a list of orders where quantities are greater than 0 and,
        lengths less or equal to the available activity length.

        :param a: current activity array

        :return: an array of fittable orders
        """
        fittable_orders = [rl for rl, q in orders.items() if q > 0 and rl <= a[0] - sum(a[1:])]
        return fittable_orders

    def plot_gaussian(self, k=500, pop=None, iterations=None):
        """
        Plots the gaussian distribution.

        :param k: size of population
        :param pop: the population fitness
        :param iterations: number of iterations

        :return:
        """
        if pop is None:
            pop = []
            for i in range(k):
                pop.append(self.get_fitness(self.random_candidate()))

        pop = pop

        mean = np.mean(pop)
        std_dev = np.std(pop)

        x_values = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 100)
        gaussian_curve = stats.norm.pdf(x_values, mean, std_dev)

        lower_bound = mean - 1*std_dev
        upper_bound = mean + 1*std_dev

        plt.hist(pop, bins=30, density=True, alpha=0.7, color='b', label="Fitness Data")
        plt.plot(x_values, gaussian_curve, color="r", label="Gaussian Distribution")
        plt.axvline(x=lower_bound, color="r", linestyle="--")
        plt.axvline(x=upper_bound, color="r", linestyle="--")
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        if iterations is not None:
            plt.title("Fitness Distribution: iteration {}.".format(iterations))
        else:
            plt.title("Fitness Distribution")
        plt.legend()
        plt.grid(True)
        plt.show()


