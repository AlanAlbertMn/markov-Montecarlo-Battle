# This is the repository for the battle between antagonist groups using Markov chanis and the Montecarlo method
# By Alan Albert

# General instructions:

- Start with a initial stochastic matrix (it can be given by the user or randomly created). In this case going from state 1 to state 2 means that a warrior from faction 1 kills a warrior from faction 2. Each entry represents how likely is one group to attack another one (for example, if the element [1][2] in the matrix is 0.60, that means there's a 60% of probability that group 1 attacks group 2).
- The number of warriors for each faction can be given by the user or randomly distributed.
- To decide which faction attacks on each turn you must generate a uniform random number. For example, if 3 factions are fighting, the random number '2' means that faction 2 is attacking. From this point to decide which faction is being attacked, use the Monte Carlo method given in class.
- Each time a group dies, the stochastic matrix must be reconfigured.
- There can be just one winner in the battle (the one that has at least one warrior left)