import random
import multiprocessing
import matplotlib.pyplot as plt


def initiate(size_pop):
    population = []
    for _ in range(0, size_pop):
        series = [random.randint(0, 1) for _ in range(0, size_l)]
        population.append(series)
    return population


def roulette(population):
    sum = 0
    sum_arr = []
    for series in population:
        sum = sum + fit_func_1(series)
        sum_arr.append(sum)
    f = random.randint(0, sum)
    for index in range(1, len(population)):
        if sum_arr[index - 1] < f <= sum_arr[index]:
            return population[index]
    return population[0]


def fit_func_1(series):
    return series.count(1)


def fit_func_2(series):
    sum = 0
    for i in range(0, size_l):
        sum += series[i] * pow(2, size_l - 1 - i)
    return sum


def mutate(series, mutation_chance):
    for gene in range(0, len(series)):
        if int(random.random() <= mutation_chance):
            if series[gene] == 1:
                series[gene] = 0
            else:
                series[gene] = 1
    return series


def crossover(a, b):
    crossover_point = random.randint(1, size_l)
    a, b = a[crossover_point:] + b[:crossover_point], a[:crossover_point] + b[crossover_point:]
    return a, b


print("Exercise 1")

size_l = 100
crossover_chance = [0.9, 0.7, 0.4, 0]


def exercise_1_run(cross_chance):
    size_pop = 100
    mutation_chance = 0.001
    sum_generation = 0
    for i in range(0, 20):
        print(i, " with crossover chance: ", cross_chance)
        flag = False
        population = initiate(size_pop)
        count = 0
        while True:
            count += 1
            temp_population = []
            for _ in range(0, int(size_pop / 2)):

                parent1 = roulette(population)
                parent2 = roulette(population)

                if random.random() < cross_chance:
                    child1, child2 = crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2

                temp_population.append(mutate(child1, mutation_chance))
                temp_population.append(mutate(child2, mutation_chance))

            population = temp_population.copy()
            for series in population:
                if series.count(1) == size_l:
                    sum_generation += count
                    flag = True
                    break

            if flag:
                break

    print("The average generation where the full series is ones, is: ", float(sum_generation) / 20,
          " with crossover chance equal to: ", cross_chance)


p = multiprocessing.Pool(4)
p.map(exercise_1_run, crossover_chance)


def exercise_2_run(cross_chance, size_pop, mutation_chance):
    population = initiate(size_pop)
    max_series = []
    avg_series = []
    for generation in range(0, 100):
        temp_population = []
        for _ in range(0, int(size_pop / 2)):

            parent1 = roulette(population)
            parent2 = roulette(population)

            if random.random() < cross_chance:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2

            temp_population.append(mutate(child1, mutation_chance))
            temp_population.append(mutate(child2, mutation_chance))

        population = temp_population.copy()
        max = 0
        sum_series = 0
        for series in population:
            fitness = fit_func_2(series)
            sum_series += fitness
            if max < fitness:
                max = fitness

        max_series.append(max)
        avg_series.append(float(sum_series) / 100)
    fig, axs = plt.subplots(2)
    title = 'Max and Average number for crossover prob: ' + str(cross_chance) + ' population: ' + str(size_pop) + ' mutation prob: ' + str(mutation_chance)
    fig.suptitle(title)
    y = [i for i in range(0, 100)]
    axs[0].plot(max_series, y)
    axs[1].plot(avg_series, y)
    plt.show()


print("Exercise 2")
# crossover chance changes
for i in [0, 0.4, 0.7, 1.0]:
    exercise_2_run(i, 100, 0.001)

# population_changes
for i in [10, 40, 100, 200]:
    exercise_2_run(0.7, i, 0.001)

# mutation chance changes
for i in [0.001, 0.08, 0.1]:
    exercise_2_run(0.7, 100, i)

