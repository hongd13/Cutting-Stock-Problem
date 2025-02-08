# Cutting-Stock-Problem
The Cutting Stock Problem (CSP) is a classic optimisation problem in operations research and industrial engineering. It involves cutting large stock materials (like paper, metal, or wood) into smaller pieces of specified sizes to meet customer demands. The goal is to determine the optimal cutting patterns that most efficiently fulfil the required orders. 

## Problem Definition
In this implementation, the problem is described as arrays of stock lengths, the associated costs per unit, the requested lengths by clients and their associated quantities:
```python
cutting_problem_example = {
  "l": [10, 13, 15],  # stock lengths
  "c": [100, 130, 150],  # stock costs
  "rl": [3, 4, 5, 6, 7, 8, 9, 10],  # requested lengths
  "q": [5, 2, 1, 2, 4, 2, 1, 3]  # requested quantities
}
```
In the example above, the problem states that a stock unit of length 10 costs 100, and clients have requested five units of length 3.

## Solution Definition
A potential solution, also known as a candidate, is defined as a dynamic array of activities, where an activity is an array that encompasses a chosen stock length followed by requested lengths:
```python
Candidate=[activity0, activity1, ..., activityX]
Activity=[l, rl0, rl1, ..., rlY]
```
The fitness is calculated by summing the costs of every chosen stock length in a candidate, notice waste does not necessarily influence the fitness in this case:
```python
for A in C:
  fitness += A[0].cost
```
To construct a random candidate, a random stock length is chosen first. Then, the activity is filled with the remaining valid requested lengths until no more can fit and no orders remain. See "random_search.py."

# Self-Aligning Evolutionary Algorithm
In Pluchino et al.'s research on "Talent versus Luck" (2018), the findings revealed that the most successful individuals in various fields are rarely the most talented but much rather the luckiest, challenging the conventional belief in the paramount importance of individual ability. This has sparked a hypothesis that traditional elitism, often portrayed and conveyed as an obvious and standard choice in optimisation problems, may not be the only viable option after all.

This novel evolutionary algorithm aims to prove that, by granting the average candidates equal opportunities to develop, we can achieve solutions similar if not closer to the true global optimum than the traditional approach by avoiding genetic stagnation and premature convergence.

Through artificially inflating the population with the most “lucky” and “average” candidates, we can to some degree recreate the experiment’s outcome. While in the given problem instance, candidates do not have a quality factor to indicate the likelihood of improvement after a mutation, we can say that candidates who fail to improve are less lucky than those who make significant progress after each mutation. Therefore, an age parameter is introduced on candidates, wherein increments after each negative mutation attempts, then kills the candidate when it gets too old. A successful mutation resets age to 0.

When a candidate dies, some of its genetic features are preserved, then crossover is performed with the current known global optimum.  This ensures that all the surviving candidates are either the “lucky” individuals or share some genes with the current “luckiest” individual.

As seen in figure 1, where 500 candidates were randomly constructed. The fitness distribution observably aligns with the normal Gaussian distribution. The seeds are then chosen from within 1 standard deviation to the population’s mean fitness.

<p align="center">
  <img src="https://github.com/hongd13/Cutting-Stock-Problem/blob/main/Picture1.png?raw=true"/>
</p>

![alt text](https://github.com/hongd13/Cutting-Stock-Problem/blob/main/Picture1.png)

As population approaches the true global optimum, more seeds are expected to die, thus aligning the population to the known global optimum, increasing the local exploration around that solution space. Parameter kill-age can thus be used to prolong or expedite this process. 

# Ant Colony Optimisation
As observed in the problem instances, some prices do not correlate linearly to the stock length. This means that some stock lengths are cheaper than others in terms of cost per unit length. Also, some requested length combinations sum up to the stock lengths perfectly. Hence, there are potentially mathematically preferred solution combinations in terms of phenotype and genotype combination.
This presumption aligns closely with the concept of a pheromone trail depicted by ACO. Making ACO potentially a promising tool for navigating the local space effectively. 
The pheromone trail is defined as follows, where weight represents the occurrence within the population, and a[1:] represents the rl and number of occurrences within the activity in tuple format:
```python
Pheromone = {
  "pheno": {l,weight},
  "geno": {l:{a[1:]:weight}}
}
```

In each cycle, the next best candidate returns home, while leaving a trail of pheromone. It then sets off without waiting, following the existing trail. If a trail is unreachable, it is removed from the candidate’s consideration. If the trail is expended, while orders remain, fill candidates randomly. The pheromone trail will then decay according to the previously travelled distance times by the specified rate of decay. Cycles repeat until the algorithm converges.

# How to use
Install all modules in the same directory. Execute the script with:
```cmd
python cutting_problem.py --algorithm [rs/evo/aco] --custom [y/n]
```

Choose "y" to enable custom problem definition, otherwise, the default problem will be used.

If custom problem is chosen, insert parameters as prompted according to the problem format defined in [problem definition](https://github.com/hongd13/Cutting-Stock-Problem?tab=readme-ov-file#problem-definition). 

Ensure each parameter is an integer and separated with a comma without spaces in between:
> E.g. 1,2,3,4,5

The number of stock lengths and stock costs should match, and the number of requested lengths and quantities should also match. 

Ensure the highest requested length does not exceed the maximum stock length. 



# References
PLUCHINO, A., BIONDO, A.E. and RAPISARDA, A., (2018). ‘Talent versus luck: The role of randomness in success and failure’, Advances in Complex Systems.
