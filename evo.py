import numpy as np
import time


class EVO:
    def __init__(self, stocks, rng, rs):
        """
        :param stocks: dictionary of stocks
        :param rng: random number generator
        :return: None
        """
        self.rng = rng
        self.stocks = stocks
        self.rs = rs
        self.orders = {}

    """
    Initialisation:
        - Generate the first generation with the specified population size.
        - Choose seeds from the current population, who are average in quality, according to Gaussian distribution.
    Iteration:
        - Each seed mutate:
            - If mutation is positive, keep mutation as new seed. Then kill old seed.
            - If mutation is negative, kill mutation, increment seed's age by 1.
        - If seed is mature (age > M), crossover with a random elite as host. Keep offspring as new seed, kill old seed.
    Termination:
        - If target reached.
        - If time is up.
        - If iteration exceeded.
        - If convergence is reached.
    """
    def run(self, pop=None, population=500, iterations=500, t=600, target=0, m=5, mutation_strength=0.5):
        """
        Runs the evolutionary algorithm for the given number of iterations,
        or time,
        or until the target is reached.

        :param pop: predefined population
        :param iterations: number of iterations
        :param t: time
        :param target: solution fitness target
        :param population: number of population
        :param m: mature age
        :param mutation_strength: mutation strength, 1 means no mutation, 0 means complete mutation

        :return: the best solution, fitness, time elapsed (in seconds)
        """
        print("------------Evolutionary Algorithm------------")
        print("Initialisation")
        log = {"candidates": [],
               "times": []}
        start_time = time.time()
        best = []  # best candidate
        ages = {}  # age of each seed candidate, {i, age}
        seeds = self.seeds_selection(pop, population)
        go = True
        while go:
            for i in range(iterations):
                print("------------Iteration {}------------".format(i))
                best = self.rs.get_best(best, seeds)
                print(f'Current best candidate: {best}')
                log["candidates"].append(best)
                log["times"].append(time.time() - start_time)
                seeds, ages = self.next_generation(seeds, population, mutation_strength, ages, m, best)
                print("Best fitness: ", self.rs.get_fitness(best))
                if time.time() - start_time > t:
                    go = False
                    break
            go = False
        print("------------Terminating------------")
        return best, self.rs.get_fitness(best), time.time() - start_time, log

    def set_order(self, orders):
        """
        Set order

        :param orders: dictionary of orders

        :return: None
        """
        self.orders = orders

    def seeds_selection(self, pop, population):
        """
        Seeds selection using Gaussian distribution.

        :param pop: population of candidates
        :param population: number of population

        :return: seeds
        """
        print("Seed selection")
        seeds = []
        fitness = {}  # {i: fitness}
        if pop is None:
            pop = []
            for i in range(population):
                candidate = self.rs.random_candidate()
                pop.append(candidate)
                fitness[len(pop) - 1] = self.rs.get_fitness(candidate)
        else:
            for i, candidate in enumerate(pop):
                fitness[i] = self.rs.get_fitness(candidate)

        mean_fitness = np.mean(list(fitness.values()))
        std_fitness = np.std(list(fitness.values()))
        lower_bound = mean_fitness - 1*std_fitness
        upper_bound = mean_fitness + 1*std_fitness

        #  Plot gaussian graph
        #self.rs.plot_gaussian(pop=list(fitness.values()))

        for i, candidate in enumerate(pop):
            if lower_bound <= fitness[i] <= upper_bound:
                seeds.append(candidate)
        print("Seeds selection completed. \nTotal seeds: {}.".format(len(seeds)))

        return seeds

    def next_generation(self, seeds, population, strength, ages, m, best):
        """
        Mutate every seed. If population isn't full, duplicate by mutation with Gaussian selection.

        :param seeds: seeds candidates
        :param population: population size
        :param strength: mutation strength
        :param ages: ages of candidates
        :param m: mature age
        :param best: current best candidate

        :return: new population, new ages
        """
        print("Next generation in progress.")
        if not ages:  # if ages not initialised, initialise it
            for i, seed in enumerate(seeds):
                ages[i] = 0
        pop = []
        for i, candidate in enumerate(seeds):
            new_ = self.mutate(candidate, strength)
            if self.rs.get_fitness(candidate) > self.rs.get_fitness(new_):  # if mutation is better
                pop.append(new_)
                ages[i] = 0
            else:
                if ages[i] >= m:  # if candidate is too old
                    candidate = self.crossover(candidate, best)
                    ages[i] = -1
                pop.append(candidate)
                ages[i] = ages[i] + 1

        if len(pop) < population:
            seeds = self.seeds_selection(pop, population)  # seeds for refilling population
        while len(pop) < population:
            seed = self.rng.choice(seeds)
            pop.append(self.mutate(seed, strength))
            ages[len(pop)-1] = 0
        return pop, ages

    def mutate(self, candidate, mutation_strength):
        """
        Mutate the given candidate.

        :param candidate: candidate solution
        :param mutation_strength: strength

        :return: mutated candidate
        """
        temp = []
        for a in candidate:
            if self.rng.randint(0, 10) < mutation_strength*10:
                temp.append(a)
        if len(temp) != len(candidate):
            temp = self.fill_order(temp)
        return temp

    def crossover(self, host, source):
        """
        Perform crossover between host and source.

        :param host:
        :param source:

        :return: offspring candidate
        """
        orders = self.orders.copy()
        offspring = []
        for a in host:
            if self.rng.randint(0, 10) < 5:
                offspring.append(a)
                for rl in a[1:]:
                    orders[rl] = orders[rl] - 1
        for a in source:
            if self.activity_is_valid(a, orders):
                offspring.append(a)
                for rl in a[1:]:
                    orders[rl] -= 1
        offspring = self.fill_order(offspring)
        return offspring

    def activity_is_valid(self, a, orders):
        """
        Check if given activity is fittable with regard to remaining orders.

        :param a: activity
        :param orders: remaining orders

        :return: True or False
        """
        r = {}  # requested quantities within the activity, {rl, q}
        for rl in a[1:]:
            if rl in r:
                r[rl] += 1
            else:
                r[rl] = 1
        for key in r.keys():
            if orders[key] < r[key]:
                return False
        return True

    def fill_order(self, candidate):
        """
        Fill incomplete candidate randomly.

        :param candidate: candidate solution

        :return: completed candidate
        """
        orders = self.orders.copy()
        for a in candidate:
            for rl in a[1:]:
                orders[rl] -= 1
        new_ = self.rs.random_candidate(orders, candidate)
        return new_
