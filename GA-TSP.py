import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
map = {}


class Data:
    # lay du lieu tu trong file
    def __init__(self, filename):
        lines = open(filename).read().split('\n')
        i = 0
        n = 1
        for line in lines:
            i = i + 1
            if i >= 7 and line != 'EOF' and line != '':
                type1 = [float(_) for _ in line.split()]
                map[n] = type1
                n = n + 1


class GA:
    def distance(self, city1, city2):
        if city1 in map and city2 in map:
            point1 = map[city1]
            point2 = map[city2]
            distance = np.power(((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2), 0.5)
        return distance

    def routeDistance(self, route):
        distance = 0
        for i in range(0, len(route)):
            fromCity = route[i]
            toCity = None
            if i + 1 < len(route):
                toCity = route[i + 1]
            else:
                toCity = route[0]
            distance += self.distance(fromCity, toCity)
        return distance

    def routeFitness(self, route):
        fitness = 1 / float(self.routeDistance(route))
        return fitness

    def createRoute(self):
        route = random.sample(list(map), len(map))
        return route

    def initialPopulation(self, popSize):
        population = []
        for i in range(popSize):
            population.append(self.createRoute())
        return population

    def selection(self, population):
        # chon lua theo fitness = 1/distance, lua chon ngau nhien boi vong quay roullette
        # luu ti le phan tram tuong ung voi moi diem o percentFitness
        fitnessValue = 0
        for i in range(popSize):
            fitness[i] = self.routeFitness(population[i])
            fitnessValue += fitness[i]
            percentFitness[i] = fitnessValue
        for i in fitness:
            percentFitness[i] = float(percentFitness[i] * 100 / fitnessValue)
        eliteRoute = {}
        i = 0
        while i < eliteSize:
            rand = float(random.randrange(0, 10000)) / 100
            for n in percentFitness:
                if percentFitness[n] < rand <= percentFitness[n + 1]:
                    if population[n] in list(eliteRoute.values()):
                        i = i
                    else:
                        eliteRoute[i] = population[n]
                        i = i + 1
        return eliteRoute

    def crossover(self, parent1, parent2):
        child = []
        childP1 = []
        childP2 = []
        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent2))
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)
        for i in range(startGene, endGene):
            childP1.append(parent1[i])
        childP2 = [item for item in parent2 if item not in childP1]
        child = childP1 + childP2
        return child

    def crossoverPop(self, eliteRoute, eliteSize):
        children = []
        child = []
        for i in range(len(eliteRoute) - 1):
            child = self.crossover(eliteRoute[i], eliteRoute[i + 1])
            children.append(child)
        children.append(self.crossover(eliteRoute[eliteSize - 1], eliteRoute[0]))
        return children

    def mutate(self, children, mutationRate):
        for i in range(len(children)):
            if random.random() < mutationRate:
                print ('Mutant!')
                swapped = int(random.random() * len(children[i]))
                swapWith = int(random.random() * len(children[i]))
                gene1 = children[i][swapped]
                gene2 = children[i][swapWith]
                children[i][swapped] = gene2
                children[i][swapWith] = gene1
        return children

    def evaluation(self, currentGen, eliteSize, mutationRate):
        eliteRoute = self.selection(currentGen)
        crossChildren = self.crossoverPop(eliteRoute, eliteSize)
        crossChildren = self.mutate(crossChildren, mutationRate)
        nextGeneration = currentGen
        fit = {}
        for i in range(len(nextGeneration)):
            fit[i] = self.routeFitness(nextGeneration[i])
        for i in range(len(crossChildren)):
            worstfit = min(list(fit.values()))
            for j in range(len(nextGeneration)):
                if fit[j] == worstfit:
                    nextGeneration[j] = crossChildren[i]
                    fit[j] = self.routeFitness(crossChildren[i])
        return nextGeneration

    def BestIndividual(self, population):
        bestIndividual = {0: None, 1: None}
        bestDistance = 200000
        pos = 0
        for i in range(len(population)):
            if self.routeDistance(population[i]) <= bestDistance:
                bestDistance = self.routeDistance(population[i])
                pos = i
        bestIndividual[0] = population[pos]
        bestIndividual[1] = bestDistance
        return bestIndividual

print ("File data: ")
# filename = raw_input ("")
filename = "a280.tsp"
a = Data(filename)
popSize = 100
fitness = {}
percentFitness = {}
eliteSize = 50
mutationRate = 0.001
time = 300
#########

test = GA()
population = test.initialPopulation(popSize)
BestDistance = test.routeDistance(population[1])
i = 1
for i in range(time):
    population = test.evaluation(population, eliteSize, mutationRate)
    print ('Generation', i, 'best distance: ', test.routeDistance(test.BestIndividual(population)[0]))
    if BestDistance > test.BestIndividual(population)[1]:
        BestDistance = test.BestIndividual(population)[1]
        BestWay = test.BestIndividual(population)[0]
print ('population:', population)
print ('Best way:', BestWay)
print ('Best distance:', test.routeDistance(BestWay))