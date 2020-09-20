import random
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

# Use this import if you want to run the algorithm for PID with Stanley
# from PID_Stanley import *    

# Use this import if you want to run the algorithm for PID with Pure Pursuit
from PID_PurePursuit import *

# By Default, this code will use the fitness function of PID_PurePursuit

no_of_variables=4
population_size=40
Cmu=0.3
generations=100
gen_fittest = []    #List to store the fittest individual's fitness value in each generation
maximisation = False
lb = [-1, -1, -1, -1]
ub = [100, 100, 100, 100]
Pc = 0.8

class Individual():
	def __init__(self, values):
		self.individual = values
		self.fitness = fitness_function(values)
		

def make_population():
    population = [
    	Individual( [lb[i]+(ub[i]-lb[i])*(random.random()) for i in range(no_of_variables)] ) 
    	for _ in range(population_size)]
    population.sort(key=lambda x: x.fitness, reverse=maximisation)
    gen_fittest.append(population[0].fitness)
    return population



def random_generate(i, size):
    sample_space = [j for j in range(size) if j!=i]
    random.shuffle(sample_space)
    j,k = random.sample(sample_space, 2)
    return j,k


def mutate(population):
    m_population = []
    for i in range(len(population)):
        indi = [ll for ll in range(no_of_variables)]
        j,k = random_generate(i, len(population))
        for t in range(no_of_variables):
            indi[t] = population[i].individual[t] + Cmu*(population[j].individual[t]-population[k].individual[t])
            if indi[t]<lb[t]: indi[t]=lb[t]
            if indi[t]>ub[t]: indi[t]=ub[t]
        m_population.append(indi)
    return m_population


def crossover(population, m_population):
    for i in range(len(population)):
        for j in range(no_of_variables):
            if random.random()>Pc:
                m_population[i][j] = population[i].individual[j]
    temp = [Individual(i) for i in m_population]
    # temp.sort(key=lambda x: x.fitness, reverse=maximisation)
    return temp



def selection(population, m_population):
    for i in range(len(population)):
        if(maximisation):
            if(m_population[i].fitness > population[i].fitness):
                population[i] = m_population[i]
        else:
            if(m_population[i].fitness < population[i].fitness):
                population[i] = m_population[i]
    population.sort(key=lambda x: x.fitness, reverse=maximisation)
    return population



if __name__ == '__main__':
    a = time.time()
    population = make_population()
    print("Time required to make population -", time.time()-a)

    print('\nInitial population')
    print("Optimal Solution -", population[0].individual, population[0].fitness)
    print("Fitness(min, max) in current population -", population[0].fitness, population[-1].fitness)

    print("\nGoing through generations")

    pbar = tqdm(total=generations)
    for i in range(generations):
        modified_population = mutate(population)
        modified_population = crossover(population, modified_population)
        # for i in range(population_size):
        # 	print(population[i].fitness, modified_population[i].fitness)
        population = selection(population, modified_population)
        gen_fittest.append(population[0].fitness)
        # print(i+1, population[0], gen_fittest[-1])
        pbar.update(1)
    pbar.close()

    print("\nOptimal Solution -", population[0].individual)
    print("Optimal Solution fitness -", population[0].fitness)
    print("Fitness(min, max) in current population -", population[0].fitness, population[-1].fitness)
    
    plt.plot([i for i in range(len(gen_fittest))], gen_fittest)
    plt.xlabel('Generations')
    plt.ylabel('Best Fitness')
    plt.show()
    # plt.savefig(f'Graphs/{Pc}_{Cmu}.jpg')
