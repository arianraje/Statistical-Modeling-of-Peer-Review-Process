"""
The set of parameters
"""

# paper
pq_sigma = 1.

# main
NUM_SCI = 1000
NUM_CONF = 2
T = 120

# conf
acceptance_rate = 0.2
reward = 1.
cost = 1.
alpha = 5
beta = 0.
gamma = 1.2 # resources
eta = 0. # pq
N = 1

# scientist
r_mean = 5.
r_sigma = 1.5
b_mean = 0
b_sigma = 1
belief_c = 0.35  # inflate my work a bit
theta_0 = 0.
theta_1 = 1.
abtry_c = 0.1
max_abtry = 0.5
max_cap = 0.5
init_belief_pecent = 0.
