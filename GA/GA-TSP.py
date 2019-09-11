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
    def cmp(self, a, b):
        return (a > b) - (a < b)

    def check(self, child, children):
        check = 0
        for i in range(len(population)):
            if self.cmp(population[i], child) == 0:
                check = check + 1
        for i in range(len(children)):
            if self.cmp(children[i], child) == 0:
                check = check + 1
        return check

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

    def createRoute(self):
        route = random.sample(list(map), len(map))
        return route

    def initialPopulation(self, popSize):
        population = []
        popDistance = []
        for i in range(popSize):
            population.append(self.createRoute())
            popDistance.append(self.routeDistance(population[i]))
        return population, popDistance

    def selection(self, population):
        # chon lua theo fitness = 1/distance, lua chon ngau nhien boi vong quay roullette
        # luu ti le phan tram tuong ung voi moi diem o percentFitness
        fitnessValue = 0
        fitness = {}
        percentFitness = {}
        for i in range(popSize):
            fitness[i] = float(1/popDistance[i])
            fitnessValue += fitness[i]
            percentFitness[i] = fitnessValue
        for i in fitness:
            percentFitness[i] = float(percentFitness[i] * 100 / fitnessValue)
        eliteRoute = {}
        i = 0
        while i < eliteSize:
            rand = float(random.random() * 100)
            for n in percentFitness:
                if percentFitness[n] <= rand < percentFitness[n + 1]:
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
        i = 0
        while i < len(eliteRoute) - 1:
            child = self.crossover(eliteRoute[i], eliteRoute[i + 1])
            check = self.check(child, children)
            if check == 0:
                children.append(child)
                i = i + 1
            else: 
                i = i
        child = self.crossover(eliteRoute[eliteSize - 1], eliteRoute[0])
        check = self.check(child, children)
        while check != 0:
            child = self.crossover(eliteRoute[eliteSize - 1], eliteRoute[0])
            check = self.check(child, children)
        children.append(child)
        children = self.mutate(children, mutationRate)
        return children

    def mutate(self, children, mutationRate):
        for i in range(len(children)):
            if random.random() < mutationRate:
                print ('Mutant!')
                swapped = int(random.random() * len(children[i]))
                swapWith = int(random.random() * len(children[i]))
                gene1 = children[i][swapped]
                gene2 = children[i][swapWith]
                child = children[i]
                child[swapped] = gene2
                child[swapWith] = gene1
                check = self.check(child, children)
                if check == 0:
                    children[i] = child
        return children

    def evaluation(self, currentGen, curGenDis, eliteSize, mutationRate):
        eliteRoute = self.selection(currentGen)
        crossChildren = self.crossoverPop(eliteRoute, eliteSize)
        nextGeneration = currentGen
        nextGenDistance = curGenDis
        fit = {}
        for i in range(len(nextGeneration)):
            fit[i] = float(1/nextGenDistance[i])
        for i in range(len(crossChildren)):
            worstfit = min(list(fit.values()))
            for j in range(len(nextGeneration)):
                if fit[j] == worstfit:
                    nextGeneration[j] = crossChildren[i]
                    nextGenDistance[j] = self.routeDistance(crossChildren[i])
                    fit[j] = float(1/nextGenDistance[j])
        return nextGeneration, nextGenDistance

    def BestIndividual(self, population, popDistance):
        bestIndividual = {0: None, 1: None}
        bestDistance = 200000
        pos = 0
        for i in range(len(population)):
            if self.routeDistance(population[i]) <= bestDistance:
                bestDistance = popDistance[i]
                pos = i
        bestIndividual[0] = population[pos]
        bestIndividual[1] = bestDistance
        return bestIndividual

print ("File data: ")
# filename = raw_input ("")
filename = "a280.tsp"
a = Data(filename)
popSize = 100
eliteSize = 50
mutationRate = 0.001
time = 500
#########

test = GA()
population, popDistance = test.initialPopulation(popSize)
BestDistance = test.routeDistance(population[1])
i = 1
for i in range(time):
    population, popDistance = test.evaluation(population, popDistance, eliteSize, mutationRate)
    print ('Generation', i, 'best distance: ', test.routeDistance(test.BestIndividual(population, popDistance)[0]))
    if BestDistance > test.BestIndividual(population, popDistance)[1]:
        BestDistance = test.BestIndividual(population, popDistance)[1]
        BestWay = test.BestIndividual(population, popDistance)[0]
# print ('population:', population)
print('Best way:', BestWay)
print('Best distance:', test.routeDistance(BestWay))
# print('\n', popDistance)
