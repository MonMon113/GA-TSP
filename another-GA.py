import random
import numpy as np


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

    def distance(self, city1, city2):
        for i in map:
            if city1 == i:
                point1 = map[i]
            if city2 == i:
                point2 = map[i]
        distance = np.power(((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2), 0.5)
        return distance

    def routeDistance(self, individual):
        # tinh tong duong di cua ca the
        distance = 0
        for n in range(1, len(individual) + 1):
            if n >= 1 and n < len(map):
                city1 = individual[n - 1]
                city2 = individual[n]
                distance = distance + self.distance(city1, city2)
            if n == len(map):
                city1 = individual[n - 1]
                city2 = individual[0]
                distance = distance + self.distance(city1, city2)
        return distance

    def check(self, route):
        # kiem tra co phan tu bi trung nhau hay khong
        check = 0
        for i in population:
            if self.cmp(population[i], route) == 0:
                check = check + 1
        return check

    def createRoute(self):
        # tao ca the
        self.root = list(map.keys())
        random.shuffle(self.root)
        return self.root

    def initialPopulation(self, popSize):
        # tao quan the
        i = 0
        while i < popSize:
            child = self.createRoute()
            check = self.check(child)
            if check == 0:
                population[i] = child
                popDistance[i] = self.routeDistance(population[i])
                i = i + 1
            if check != 0:
                i = i
        return 0

    def selection(self, eliteSize):
        # chon lua theo fitness = 1/distance, lua chon ngau nhien boi vong quay roullette
        # luu ti le phan tram tuong ung voi moi diem o percentFitness
        fitnessValue = 0
        percentFitness = {}
        for i in popDistance:
            fitness[i] = float(1 / popDistance[i])
            fitnessValue += float(1 / popDistance[i])
            percentFitness[i] = fitnessValue
        for m in fitness:
            percentFitness[m] = float(percentFitness[m] * 100) / fitnessValue
        eliteRoute = {}
        i = 0
        while i < eliteSize:
            rand = float(random.random() * 100)
            eliteRoute[i] = 1
            for n in percentFitness:
                if percentFitness[n] < rand <= percentFitness[n + 1]:
                    eliteRoute[i] = n
            check = 0
            for m in eliteRoute:
                if eliteRoute[m] == eliteRoute[i] and m != i:
                    check = 1
            if check == 0:
                i = i + 1
            if check != 0:
                i = i
        return eliteRoute

    def crossover(self, cutRange, eliteSize):
        # lai ghep bang phuong phap doi
        i = 0
        child = {}
        dulp = 0
        # lay phan chung cua parent 1 va parent 2, range [0, cutRange]
        while i < eliteSize:
            geneRange = []
            if i == eliteSize - 1:
                j = 0
            elif i != eliteSize - 1:
                j = i + 1
            eliteRoute = self.selection(eliteSize)
            for m in range(cutRange):
                geneRange.append(population[eliteRoute[i]][m - 1])
            child[i] = geneRange
            other = 0
            while other < len(map):
                for n in range(len(geneRange)):
                    if geneRange[n] == population[eliteRoute[j]][other]:
                        dulp = dulp + 1
                if dulp == 0:
                    child[i].append(population[eliteRoute[j]][other])
                else:
                    dulp = 0
                other = other + 1
            self.mutation(child[i], mutationRate)
            check = self.check(child[i])
            if check == 0:
                i = i + 1
            if check != 0:
                i = i
        return child

    def mutation(self, child, mutationRate):
        rand = float(random.randrange(0, 10000)) / 10000
        while rand <= mutationRate:
            print('Mutant!')
            swapped = 2
            swapWith = 5
            gene1 = child[swapped]
            gene2 = child[swapWith]
            child[swapped] = gene2
            child[swapWith] = gene1
            rand = float(random.randrange(0, 10000)) / 10000
        return child

    def evaluation(self, children, eliteSize, popSize):
        i = 0
        worstFitness = {}
        while i < eliteSize:
            worstFitness[i] = 0
            for j in range(popSize):
                out = 0
                if fitness[j] <= fitness[worstFitness[i]]:
                    for n in range(len(worstFitness)):
                        if j == worstFitness[n]:
                            out = 1
                    if out == 0:
                        worstFitness[i] = j
            i = i + 1
        i = 0
        while i < eliteSize:
            population[worstFitness[i]] = children[i]
            popDistance[worstFitness[i]] = self.routeDistance(children[i])
            i = i + 1
        return 0

    def bestIndividual(self):
        bestIndividual = {0: None, 1: None}
        bestDistance = 200000
        pos = 0
        for i in range(popSize):
            if popDistance[i] <= bestDistance:
                bestDistance = popDistance[i]
                pos = i
        bestIndividual[0] = population[pos]
        bestIndividual[1] = bestDistance
        return bestIndividual


map = {}
population = {}  # danh sach quan the
popDistance = {}  # danh sach duong di cua moi ca the
fitness = {}
popSize = 100  # so ca the trong quan the
eliteSize = 50  # so ca the cha me duoc chon
time = 1000  # so the he
cutRange = 5  # diem gene cat lai ghep
mutationRate = 0.001
print("File data: ")
filename = "dj38.tsp"
a = Data(filename)

i = 1
test = GA()
test.initialPopulation(popSize)
BestDistance = test.routeDistance(population[1])
while i <= time:
    test.evaluation(test.crossover(cutRange, eliteSize), eliteSize, popSize)
    print('Generation', i, 'best distance: ', test.routeDistance(test.bestIndividual()[0]))
    if BestDistance > test.bestIndividual()[1]:
        BestDistance = test.bestIndividual()[1]
        BestWay = test.bestIndividual()[0]
    i = i + 1
# print ('population:', population)
print('Best way:', BestWay)
print('Best distance:', test.routeDistance(BestWay))
print(popDistance)
