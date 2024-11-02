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


# How to use
- Open cutting_problem.py
  - Modify line 149 to customise a problem definition.
  - Modify line 155 to choose a problem preset.
  - Modify line 164 to choose an optimisation algorithm.
 - Run cutting_problem.py
