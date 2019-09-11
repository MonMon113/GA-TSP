import random
import numpy as np

map = {}

population = {} #danh sach quan the
populationDistance = {} #danh sach duong di cua moi ca the
fitness = {}
percentFitness = {}

indiNumber = 100 #so ca the trong quan the
const = 25 #so ca the cha me duoc chon va so ca the moi duoc thay the
time = 1000 #so the he

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

	def DistanceCalculate(self, individual1, individual2):
		# tim ten thanh pho trong bang map va lay toa do cua thanh pho
		for i in map:
			if individual1 == i:
				point1 = map[i]
			if individual2 == i:
				point2 = map[i]
		distance = np.power(((point1[1]-point2[1])**2 + (point1[2]-point2[2])**2), 0.5)
		return distance

	def Distance(self, individual):
		# tinh tong duong di cua ca the
		distance = 0
		for n in range(1, len(individual)+1):
			if n >= 1 and n < len(map):
				p1 = individual[n-1]
				p2 = individual[n]
				distance = distance + self.DistanceCalculate(p1, p2)
			if n == len(map):
				p1 = individual[n-1]
				p2 = individual[0]
				distance = distance + self.DistanceCalculate(p1, p2)
		return distance

	def Check(self, child):
		# kiem tra co phan tu bi trung nhau hay khong
		check = 0
		for i in population:
			if self.cmp(population[i], child) == 0:
				check = check + 1
		return check

	def IntializationIndividual(self):
		# tao ca the
		self.root = list(map.keys())
		random.shuffle(self.root)
		return self.root

	def IntializationPopulation(self):
		# tao quan the
		number = indiNumber
		while number>0:
			population[number] = self.IntializationIndividual()
			populationDistance[number] = self.Distance(population[number])
			number = number - 1
		return population

	def Selection(self):
		# chon lua theo fitness = 1/distance, lua chon ngau nhien boi vong quay roullette
		# luu ti le phan tram tuong ung voi moi diem o percentFitness
		fitnessValue = 0
		for i in populationDistance:
			fitness[i] = float(1/populationDistance[i])
			fitnessValue += float(1/populationDistance[i])
			percentFitness[i] = fitnessValue
		for m in fitness:
			percentFitness[m] = float(percentFitness[m]*100)/fitnessValue
		parent = {}
		i = 1
		while const >= i:
			rand = float(random.randrange(0, 10000))/100
			parent[i] = 1
			for n in percentFitness:
				if percentFitness[n] < rand and percentFitness[n-1] >= rand:
					parent[i] = n - 1
			out = 0
			for m in parent:
				if parent[m] == parent[i] and m != i:
					out = 1
			if out == 0:
				i = i + 1
			if out != 0:
				i = i
		return parent

	def Crossover(self, cutRange):
		#lai ghep bang phuong phap doi
		a = 1
		child = {}
		dulp = 0
		#lay phan chung cua parent 1 va parent 2, range [0, cutRange]
		while const >= a:
			ConstRange =[]
			if a == const:
				b = 1
			if a != const:
				b = a+1
			parentID = self.Selection()
			for i in population:
				if parentID[a] == i:
					# ConstRange = np.copy(population[i][0:cutRange])
					for m in range(cutRange):
						ConstRange.append(population[i][m-1])
			child[a] = ConstRange

			#chep phan con lai cua parent 2 vao child 1
			other = 0
			while other < len(map):
				for n in range(len(ConstRange)):
					if ConstRange[n-1] == population[parentID[b]][other]:
						dulp = dulp + 1
				if dulp == 0:
					# child[a] = np.concatenate([child[a], np.array([population[parentID[b]][other]])])
					child[a].append(population[parentID[b]][other])
				else:
					dulp = 0
				other = other + 1
			rand1 = float(random.randrange(0, 10000))/10000
			while rand1 <= 0.001:
				self.Mutation(child[a], rand1)
				rand1 = float(random.randrange(0, 10000))/10000
			check = self.Check(child[a])
			if check == 0:
				a = a + 1
			if check != 0:
				a = a
		return child

	def Mutation(self, child, fit):
		if fit <= 0.001:
			print ('Mutant!')
			MutantGen = child[2]
			MutantGen2 = child[5]
			child[2] = MutantGen2
			child[5] = MutantGen
			return child
		else:
			return child

	def Evaluation(self, child):
		r = 1
		worstFitness = {}
		while const >= r:
			worstFitness[r] = 0
			for i in range(len(fitness)):
				out = 0
				fitness[0] = 1
				if fitness[i] <= fitness[worstFitness[r]]:
					for n in range(1, len(worstFitness)+1):
						if i == worstFitness[n]:
							out = 1
					if out == 0:
						worstFitness[r] = i
			r = r + 1
		del fitness[0]

		r = 1
		while const >= r:
			population[worstFitness[r]] = child[r]
			populationDistance[worstFitness[r]] = self.Distance(child[r])
			r = r + 1
		return population

	def BestIndividual(self):
		bestIndividual = {0: None, 1: None}
		bestDistance = 200000
		pos = 0
		for i in range(1, len(populationDistance)+1):
			# print populationDistance[i]
			if populationDistance[i] <= bestDistance:
				bestDistance = populationDistance[i]
				pos = i
		bestIndividual[0] = population[pos]
		bestIndividual[1] = bestDistance
		return bestIndividual

if __name__ == '__main__':
	print ("File data: ")
	# filename = raw_input ("")
	filename = "kroA100.tsp"
	a = Data (filename)

	i = 1
	cutRange = 5
	test = GA()
	test.IntializationPopulation()
	BestDistance = test.Distance(population[1])
	while time >= i:
		test.Evaluation(test.Crossover(cutRange))
		print ('Generation',i,'best distance: ', test.Distance(test.BestIndividual()[0]))
		if BestDistance > test.BestIndividual()[1]:
			BestDistance = test.BestIndividual()[1]
			BestWay = test.BestIndividual()[0]
		i = i+1
	print ('population:', population)
	print ('Best way:', BestWay)
	print ('Best distance:', test.Distance(BestWay))
