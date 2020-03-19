import numpy
from multiprocessing import Process, Pool

equation_inputs = [4, -2, 3.5, 5, -11, -4.7]


def function(pop):
    numbers = numpy.hsplit(pop, (1,))[0]
    vars = numpy.hsplit(pop, (1,))[1]

    # print('Varrrrrrrrrrrrrrrs', vars)

    fitness = numpy.sum(vars * equation_inputs, axis=1)
    # print(fitness)
    fitness_2 = numpy.column_stack((numbers, fitness))

    return fitness_2


def cal_pop_fitness(equation_inputs, pop, workers=8):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function caulcuates the sum of products between each input and its corresponding weight.
    pop_arg = numpy.copy(pop)
    numbers = numpy.array([[i] for i in range(pop_arg.shape[0])])
    # print('Numbbbbbbeers', numbers)

    numbers = numpy.column_stack((numbers, pop_arg))
    # print('Poooooop', pop_arg)
    # print('Numbbbbbbeers', numbers)

    args = numpy.array_split(numbers, workers)
    # numbers = [i for i in range(workers)]
    outputs = numpy.array([-1, 1])

    # if __name__ == '__main__':

    #with Pool(workers) as p:
    #print('ssssttttaaarrrrttt')
    p = Pool(workers)
    #print('finnnnnnnnnnnnnnn')
    results = p.map(function, args)
    #print('TTTTTTTTTTTTTTTWOWOWOWOW', results)


    for res in results:
        outputs = numpy.row_stack((outputs, res))
    # print('RESSSSSS', results)

    # outputs_sort = outputs[numpy.argsort(outputs[:, 0])]
    # print('SSHHHHHAPPPE', outputs)
    fitness_2 = numpy.array([])
    #print('NOOOORRRRRRRRRRRMMMMMMMM')
    #if outputs.shape[0] > 2:
    outputs_sort = outputs[numpy.argsort(outputs[:, 0])]
    fitness_2 = outputs_sort.T
    fitness_2 = fitness_2[1:]
    fitness_2 = fitness_2[0][1:]
    # print('SSSSSSSSSSSSSSSS', fitness_2.shape)
    # print('FFFFFFFFFFFFFFF', fitness_2)
    # fitness = numpy.sum(pop*equation_inputs, axis=1)
    # print(fitness)
    return fitness_2
'''else:
         print('ERRRRRREERR: ')
         return numpy.sum(pop * equation_inputs, axis=1)'''


def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents


def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually it is at the center.
    crossover_point = numpy.uint8(offspring_size[1] / 2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k % parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k + 1) % parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring


def mutation(offspring_crossover):
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offspring_crossover.shape[0]):
        # The random value to be added to the gene.
        random_value = numpy.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, 4] = offspring_crossover[idx, 4] + random_value
    return offspring_crossover


"""
The y=target is to maximize this equation ASAP:
    y = w1x1+w2x2+w3x3+w4x4+w5x5+6wx6
    where (x1,x2,x3,x4,x5,x6)=(4,-2,3.5,5,-11,-4.7)
    What are the best values for the 6 weights w1 to w6?
    We are going to use the genetic algorithm for the best possible values after a number of generations.
"""

# Inputs of the equation.


# Number of the weights we are looking to optimize.
num_weights = 6

"""
Genetic algorithm parameters:
    Mating pool size
    Population size
"""
sol_per_pop = 10
num_parents_mating = 4
num_generations = 1000

# Defining the population size.
pop_size = (sol_per_pop,
            num_weights)  # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
# Creating the initial population.
new_population = numpy.random.uniform(low=-4.0, high=4.0, size=pop_size)
# print(new_population)
if __name__ == '__main__':
    fitness = cal_pop_fitness(equation_inputs, new_population)


    for generation in range(num_generations):
        print("Generation : ", generation)
        # Measing the fitness of each chromosome in the population.
        fitness = cal_pop_fitness(equation_inputs, new_population)

        # Selecting the best parents in the population for mating.
        parents = select_mating_pool(new_population, fitness,
                                     num_parents_mating)

        # Generating next generation using crossover.
        offspring_crossover = crossover(parents,
                                        offspring_size=(pop_size[0] - parents.shape[0], num_weights))

        # Adding some variations to the offsrping using mutation.
        offspring_mutation = mutation(offspring_crossover)

        # Creating the new population based on the parents and offspring.
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_mutation

        # The best result in the current iteration.
        print("Best result : ", numpy.max(numpy.sum(new_population * equation_inputs, axis=1)))

    # Getting the best solution after iterating finishing all generations.
    # At first, the fitness is calculated for each solution in the final generation.
    fitness = cal_pop_fitness(equation_inputs, new_population)
    # Then return the index of that solution corresponding to the best fitness.
    best_match_idx = numpy.where(fitness == numpy.max(fitness))

    print("Best solution : ", new_population[best_match_idx, :])
    print("Best solution fitness : ", fitness[best_match_idx])
