import numpy as np
import copy
import time


class ACO:
    def __init__(self, stocks, rng, rs, evo):
        """
        :param stocks: dictionary of stocks
        :param rng: random number generator
        :param rs: random search model
        :param evo: evolution model

        :return:
        """
        self.stocks = stocks
        self.rng = rng
        self.rs = rs
        self.evo = evo
        self.orders = {}

    """
    Initialisation:
        - Generate a colony of population.
    Cycle:
        - The next best candidate returns to home, leaving a trail of pheromone, then sets off following the trail.
        - At the end of each cycle, pheromone trail decays slightly.
    Termination:
        - If cycle exceeded.
        - If time is up.
        - If target is reached.
    """
    def run(self, pop=None, population=100, cycles=500, decay=-0.5):
        """
        Run the ACO algorithm.

        :param pop: predefined population
        :param population: population size
        :param cycles: number of cycles (travels)
        :param decay: rate of decay

        :return:
        """
        print("------------------ACO------------------")
        print("Initialisation")
        log = {"candidates": [],
               "times": []}
        if pop is None:  # if population not predefined
            print("Initialising colony.")
            pop = []
            for i in range(population):
                pop.append(self.rs.random_candidate())
        start_time = time.time()
        rank_f = self.update_fitness(pop)  # sorted dictionary {index from pop: fitness}
        best = []  # best candidate
        convergence = 2*len(pop)
        go = True
        while go:
            pheromone = {}
            for i in range(cycles):
                print("------------Cycle {}------------".format(i))
                i = next(iter(rank_f))  # index of next candidate to return home and set off
                if not best or self.rs.get_fitness(best) > self.rs.get_fitness(pop[i]):
                    best = pop[i]
                    log["candidates"].append(best)
                    log["times"].append(time.time() - start_time)
                    convergence = 2*len(pop)
                else:
                    convergence -= 1
                    print(convergence)
                    if convergence <= 0:
                        print("Converged.")
                        go = False
                        break
                print("Best fitness: ", self.rs.get_fitness(best))
                pheromone = self.update_trail(pop[i], pheromone)
                pop[i] = self.set_off(pheromone)
                rank_f = self.update_fitness(c=pop[i], rank=rank_f)  # ranked fitness
                pheromone = self.decay(pheromone, decay)
            go = False
        return best, self.rs.get_fitness(best), time.time() - start_time, log

    def run_iterative(self, pop=None, population=100, cycles=500, decay=-0.5, iterations=100):
        """
        Run the ACO algorithm iteratively.

        :param pop:
        :param population:
        :param cycles:
        :param decay:
        :param iterations:

        :return:
        """
        print("------------------Iterative ACO------------------")
        best, fitness, run_time, log = None, None, None, None
        for i in range(iterations):
            print("--------------Iteration {}--------------".format(i))
            if i == 0:
                best, fitness, run_time, log = self.run(pop=pop, cycles=cycles, decay=decay)
            for j in range(population):
                pop = self.rs.random_candidate()
            pop[0] = best
            best, fitness, run_time, log = self.run(pop=pop, cycles=cycles, decay=decay)
        return best, fitness, run_time, log

    def set_order(self, orders):
        """
        Set order

        :param orders: dictionary of orders

        :return: None
        """
        self.orders = orders

    def update_fitness(self, pop=None, rank=None, c=None):
        """
        Updates the fitness ranking dictionary.

        :param pop: array of candidates
        :param rank: array of previous ranks {i: f}
        :param c: new candidate

        :return: sorted fitness dictionary
        """
        fitnesses = {}  # dict of fitness
        if pop is not None:
            for i, c in enumerate(pop):
                fitnesses[i] = self.rs.get_fitness(c)
        else:
            fitnesses = rank
            i = next(iter(fitnesses))
            prev = fitnesses[i]
            for j in range(len(fitnesses)):
                fitnesses[j] -= prev
            fitnesses[i] = self.rs.get_fitness(c)
        sorted_f = dict(sorted(fitnesses.items(), key=lambda item: item[1]))
        return sorted_f

    def update_trail(self, c, pheromone):
        """
        Return a new pheromone trail.

        :param c: candidate
        :param pheromone: previous pheromone {{phenotype space}, {genotype space}}

        :return: updated pheromone trail
        """
        print("Leaving trail...")
        if not pheromone:  # if pheromone trail is empty
            pheromone = {"pheno": {},  # {l: weight}
                         "geno": {}}  # {l: {[rl..]: weight}}
        for a in c:
            pheromone["pheno"][a[0]] = pheromone["pheno"].get(a[0], 0) + 1
            rl_counter = {}
            for rl in a[1:]:
                rl_counter[rl] = rl_counter.get(rl, 0) + 1
            sorted_counter = dict(sorted(rl_counter.items()))
            rl_tuple = tuple(sorted_counter.items())
            pheromone["geno"][a[0]] = pheromone["geno"].get(a[0], {})
            pheromone["geno"][a[0]][rl_tuple] = pheromone["geno"][a[0]].get(rl_tuple, 0) + 1
        return pheromone

    def set_off(self, pheromone):
        """
        Candidate follows the given pheromone trail.

        :param pheromone: pheromone trail

        :return: new candidate
        """
        print("Following pheromone trail...")
        c = []
        p = copy.deepcopy(pheromone)
        orders = self.orders.copy()
        while sum(orders.values()) > 0:  # while orders remaining
            if not p["geno"]:
                c = self.evo.fill_order(c)
                return c
            a = []
            weights = [num / sum(list(p["pheno"].values())) for num in list(p["pheno"].values())]  # pheno weights
            a.append(int(np.random.choice(list(p["pheno"].keys()), 1, p=weights)))  # stock length
            weights = [num / sum(list(p["geno"][a[0]].values())) for num in list(p["geno"][a[0]].values())]  # geno weights
            keys = list(p["geno"][a[0]].keys())
            geno_key = int(np.random.choice([i for i in range(len(keys))], 1, p=weights))
            geno_dict = dict(keys[geno_key])
            geno_array = []
            for key in geno_dict.keys():
                for i in range(int(geno_dict[key])):
                    geno_array.append(key)
            a = a + geno_array
            if self.evo.activity_is_valid(a, orders):
                c.append(a)
                for rl in a[1:]:
                    orders[rl] -= 1
            else:  # chosen activity not valid
                p["geno"][a[0]].pop(keys[geno_key], None)
                if not p["geno"][a[0]]:
                    p["geno"].pop(a[0], None)
                    p["pheno"].pop(a[0], None)
        return c

    def decay(self, p, d):
        """
        Decay the pheromone trail by the specified amount

        :param p: previous pheromone
        :param d: rate of decay

        :return: updated pheromone
        """
        for pheno in list(p["pheno"].keys()):
            p["pheno"][pheno] += d
            if p["pheno"][pheno] <= 0:
                p["pheno"].pop(pheno, None)
        for stock in list(p["geno"].keys()):
            for geno in list(p["geno"][stock].keys()):
                p["geno"][stock][geno] += d
                if p["geno"][stock][geno] <= 0:
                    p["geno"][stock].pop(geno, None)
        return p
