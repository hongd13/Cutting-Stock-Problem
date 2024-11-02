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
In the example above, the problem states that a stock unit of length 10 costs 100, and clients have requested five units of length 5.

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

# Evolutionary Algorithm
In Pluchino et al.'s (2018) research on "Talent versus Luck," the findings revealed that the most successful individuals in various fields are almost never the most talented ones, but much rather the luckiest, challenging the conventional belief in the paramount importance of individual ability. This has sparked a hypothesis that perhaps, the traditional elitism, often portrayed and conveyed as an obvious and standard choice in the optimisation problems may not be the only viable option after all.

This novel evolutionary algorithm aims to prove that, by granting the average candidates equal opportunities to develop, we can achieve solutions similar if not closer to the true global optimum than the traditional approach by avoiding genetic stagnation and premature convergence.

Through artificially inflating the population with the most “lucky” and “average” candidates, we can to some degree recreate the experiment’s outcome. While in the given problem instance, candidates do not have a quality factor to indicate the likelihood of improvement after a mutation, we can say that candidates who fail to improve are less lucky than those who make significant progress after each mutation. Therefore, an age parameter is introduced on candidates, wherein increments after each negative mutation attempts, then kills the candidate when it gets too old. A successful mutation resets age to 0.

When a candidate dies, some of its genetic features are preserved, then crossover is performed with the current known global optimum.  This ensures that all the surviving candidates are either the “lucky” individuals or share some genes with the current “luckiest” individual.

As seen in figure 1, where 500 candidates were randomly constructed. The fitness distribution observably aligns with the normal Gaussian distribution. The seeds are then chosen from within 1 standard deviation to the population’s mean fitness.

![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)

As population approaches the true global optimum, more seeds are expected to die, thus aligning the population to the known global optimum, increasing the local exploration around that solution space. Parameter kill-age can thus be used to prolong or expedite this process. 


# How to use
- Open cutting_problem.py
  - Modify line 149 to customise a problem definition.
  - Modify line 155 to choose a problem preset.
  - Modify line 164 to choose an optimisation algorithm.
 - Run cutting_problem.py

# References
PLUCHINO, A., BIONDO, A.E. and RAPISARDA, A., (2018). ‘Talent versus luck: The role of randomness in success and failure’, Advances in Complex Systems.
