import numpy as np
from util import construct_robots_and_simulate_behaviors
from util_fitness_and_metrics import calculate_fitness_and_metrics


def select_survivors(individuals, fitness_and_metrics):
    average = [162.29714514585564, 0.10415503229916442, 4.489081892093979, 0.0715434096704684]
    std_dev = [46.79208827751169, 0.03886989349782155, 1.6752924097561088, 0.037130429051313626]
    nr_of_buckets = [10, 10, 10, 10]
    minn = []; maxx = []; size_of_the_buckets = []
    for i in range(0, 4):
        minn.append(average[i] - std_dev[i] * 1.5)
        maxx.append(average[i] + std_dev[i] * 1.5)
        size_of_the_buckets.append((maxx[i] - minn[i]) / nr_of_buckets[i])

    max_fitness = 0
    map = dict()
    for i in range(len(individuals)):
        if all(fitness_and_metrics[i][j+1] is not None for j in range(4)):
            bucket = [0, 0, 0, 0]
            for j in range(4):
                x = (fitness_and_metrics[i][j+1] - minn[j]) // size_of_the_buckets[j]
                x = max(min(x, nr_of_buckets[j] - 1), 0)
                bucket[j] = x
            number = bucket[0] * 1000 + bucket[1] * 100 + bucket[2] * 10 + bucket[3]
            if number not in map.keys() or fitness_and_metrics[i][0] > fitness_and_metrics[map[number]][0]:
                map[number] = i
                max_fitness = max(max_fitness, fitness_and_metrics[i][0])

    p = 0.4
    for i in range(5, 15):
        if len(map) >= i * 10:
            p += 0.05

    survivors = []
    survivors_fitness_and_metrics = []
    survivors_bucket_number = []
    for key in map.keys():
        index = map[key]
        if fitness_and_metrics[index][0] >= max_fitness * p:
            survivors.append(individuals[index])
            survivors_fitness_and_metrics.append(fitness_and_metrics[index])
            survivors_bucket_number.append(key)

    return survivors, survivors_fitness_and_metrics, survivors_bucket_number


def select_parents(individuals, fitness_and_metrics):
    parents = []
    parents_fitness_and_metrics = []

    tournament_size = 3
    for i in range(2 * len(individuals)):
        random_numbers = np.random.choice(np.arange(len(individuals)), size=tournament_size, replace=True)
        best_fitness = 0
        best_individual = None
        for j in random_numbers:
            if fitness_and_metrics[j][0] > best_fitness:
                best_fitness = fitness_and_metrics[j][0]
                best_individual = j
        parents.append(individuals[best_individual])
        parents_fitness_and_metrics.append(fitness_and_metrics[best_individual])

    return parents, parents_fitness_and_metrics


def uniform_crossover(parent1, parent2):
    mask = np.random.choice([True, False], size=len(parent1))
    offspring = np.where(mask, parent1, parent2)
    return offspring

def average_crossover(parent1, parent2):
    offspring = []
    for i in range(len(parent1)):
        offspring.append((parent1[i] + parent2[i]) / 2)
    return offspring

def crossover(parents):
    offsprings = []
    for i in range(0, len(parents), 2):
        offspring = uniform_crossover(parents[i], parents[i + 1])
        offsprings.append(offspring)
    return offsprings

def mutate_and_calculate_fitness_and_metrics(offsprings):
    for i in range(len(offsprings)):
        for j in range(len(offsprings[i])):
            offsprings[i][j] += np.random.normal(loc=0, scale=0.1)

    robots, behaviors = construct_robots_and_simulate_behaviors(offsprings)
    offsprings_fitness_and_metrics = calculate_fitness_and_metrics(robots, behaviors)

    return offsprings, offsprings_fitness_and_metrics

