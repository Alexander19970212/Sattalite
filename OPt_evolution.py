import numpy as np

pop = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
fitness = np.array([1, 2, 3, 4])
elitist_fraction = 2

pop = pop[np.argsort(-fitness)[-elitist_fraction:], :]
print(pop)