import numpy as np
import sim-tools

from sim_tools.distributions import Exponential, Normal

rng = np.random.default_rng()
print(rng.exponential(scale=17, size=3))

rng = np.random.default_rng(20)
print(rng.exponential(scale=17, size=3))

rng = np.random.default_rng(20)
print(rng.exponential(scale=17, size=6))
