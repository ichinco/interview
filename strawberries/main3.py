from Field import Field
from Solution import Solution, Greenhouse
from queue import Queue
from ComboCache import ComboCache
import cProfile
from PrettySolution import PrettySolution

matrix = ("..@@@@@...............\n" +
			"..@@@@@@........@@@...\n" +
			".....@@@@@......@@@...\n" + 
			".......@@@@@@@@@@@@...\n" +
			".........@@@@@........\n" +
			".........@@@@@........" )

n = 4

interesting=[18,70,325,415]

def findForN(n, field):	
	previousSolution = None
	currentSolution = PrettySolution(field.getRandomCoords(n))
	for point in field.getCoords():
		currentSolution.addPointToCluster(point)	

	iteration = 0
	while (previousSolution == None or not(previousSolution == currentSolution) and iteration < 1000):
		previousSolution = currentSolution
		currentSolution = PrettySolution(previousSolution.getNewClusterCenters())
		for point in field.getCoords():
			currentSolution.addPointToCluster(point)
			
		iteration = iteration + 1
		
	return currentSolution	

def findSolution(n, matrix):
	field = Field()
	field.createField(matrix)
	print(n)
	field.printField()
	
	currentBest = None

	for i in range(1,n+1):
		for j in range(5):
			newSolution = findForN(i, field)
			if (currentBest == None or newSolution.getCost() < currentBest.getCost()):
				currentBest = newSolution
			
	currentBest.printSolution(field.getMaxX(),field.getMaxY())

f = open('rectangles.txt')
wholeFile = f.read()
tasks = wholeFile.split("\n\n")
for task in tasks:
	lines = task.split("\n")
	n = int(lines[0])
	matrix = "\n".join(lines[1:])
	findSolution(n,matrix)
