import numpy as np

from sim_tools.distributions import Exponential, Normal

rng = np.random.default_rng()
print(rng.exponential(scale=17, size=3))

rng = np.random.default_rng(20)
print(rng.exponential(scale=17, size=3))

rng = np.random.default_rng(20)
print(rng.exponential(scale=17, size=6))

arrivals_exp = Exponential(mean=3, random_seed=1)
processing_norm = Normal(mean=10, sigma=2, random_seed=2)

'''Using Simtools distributions to sample'''
arrivals = arrivals_exp.sample(3)
processing = processing_norm.sample(3)
print(f"Arrivals: {arrivals}\nProcessing: {processing}")

arrivals_exp = Exponential(mean=3, random_seed=1)
processing_norm = Normal(mean=10, sigma=2, random_seed=2)
arrivals = arrivals_exp.sample(5)
processing = processing_norm.sample(3)

print(f"Arrivals: {arrivals}\nProcessing: {processing}")