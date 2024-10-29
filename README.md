# Cutting-Stock-Problem
The Cutting Stock Problem (CSP) is a classic optimisation problem in operations research and industrial engineering. It involves cutting large stock materials (like paper, metal, or wood) into smaller pieces of specified sizes to meet customer demands. The goal is to determine the optimal cutting patterns that most efficiently fulfil the required orders. 

In this implementation, the problem is described as arrays of stock lengths, the associated costs per unit, the requested lengths by clients and their associated quantities:
```python
cutting_problem = {
  "l": [],  # stock lengths
  "c": [],  # stock costs
  "rl": [],  # requested lengths
  "q": []  # requested quantities
}
```

# How to use
- Open cutting_problem.py
  - Modify line 149 to customise a problem definition.
  - Modify line 155 to choose a problem preset.
  - Modify line 164 to choose an optimisation algorithm.
 - Run cutting_problem.py
