
from Field import Field
from Solution import Solution, Greenhouse
from queue import Queue
from ComboCache import ComboCache
import cProfile

matrix = ("..@@@@@...............\n" +
			"..@@@@@@........@@@...\n" +
			".....@@@@@......@@@...\n" + 
			".......@@@@@@@@@@@@...\n" +
			".........@@@@@........\n" +
			".........@@@@@........" )

n = 4

interesting=[18,70,325,415]

def findSolution(n, matrix):
	field = Field()
	field.createField(matrix)
	print(n)
	field.printField()

	solutions = Queue()

	minSolution = None
	solution = Solution(field)
	
	greenhouses = []
	for i in range(len(field.getCoords())):
		corner1 = field.getCoords()[i]
		for j in range(i,len(field.getCoords())):
			corner2 = field.getCoords()[j]
			greenhouse = Greenhouse(corner1.x,corner2.x,corner1.y,corner2.y)
			for coord in field.getCoords():
				if greenhouse.containsCoord(coord.x, coord.y):
					greenhouse.addContainedCoordinate(coord)
			if (greenhouse.getWastedCoordinates() < 10):
				greenhouses.append(greenhouse)
			# if (corner1.y==6 and corner1.x==2 and 
				# greenhouse.getNumberOfContainedCoordinates() == 10 and
				# greenhouse.getWastedCoordinates() == 0):
				# solution = []
				# solution.append(greenhouse)
				# newSolution = Solution(field)
				# newSolution.setGreenhouses(solution)
				# print(len(greenhouses))
				# newSolution.printSolution()			
								
	sorted(greenhouses, key=Greenhouse.getWastedCoordinates, reverse=True)
	nextQueue = Queue()
			
	for i in range(1,n+1):
		print(i)
		if (not nextQueue.empty()):
			solutions = nextQueue
		else:
			solutions.put((0,[]))
		
		while(not solutions.empty()):
			# print(solutions.qsize())
			sol = solutions.get()
			index = sol[0]
			solution = sol[1]
			
			if (len(solution) == i-1):
				# nextQueue.put((0,list(solution)))
				left = None
				right = None
				top = None
				bottom = None
				for coord in field.getCoords():
					inGreenhouse = False
					for greenhouse in solution:
						inGreenhouse = inGreenhouse or greenhouse.containsCoord(coord.x,coord.y)
					if (not inGreenhouse):
						if (left == None or coord.x < left):
							left = coord.x
						if (right == None or coord.x > right):
							right = coord.x
						if (top == None or coord.y < top):
							top = coord.y
						if (bottom == None or coord.y > bottom):
							bottom = coord.y
				
				if (not left == None):
					greenhouse = Greenhouse(left,right,top,bottom)
								
					overlaps = False
					for setGreenhouse in solution:
						if (setGreenhouse.overlaps(greenhouse)):
							overlaps = True
							break
					
					if (not overlaps):
						solution.append(greenhouse)
						newSolution = Solution(field)
						newSolution.setGreenhouses(solution)
						if (minSolution == None or newSolution.computeCost() < minSolution.computeCost()):
							minSolution = newSolution
				
			else:
				for ind in range(len(greenhouses)):
					overlaps = False
					greenhouse = greenhouses[ind]
					for setGreenhouse in solution:
						if (setGreenhouse.overlaps(greenhouse)):
							overlaps = True
							break
					
					if (not overlaps):
						newSolution = list(solution)
						newSolution.append(greenhouse)
						solutions.put((ind,newSolution))
						
	minSolution.printSolution()

f = open('rectangles.txt')
wholeFile = f.read()
tasks = wholeFile.split("\n\n")
task = tasks[2]
lines = task.split("\n")
n = int(lines[0])
matrix = "\n".join(lines[1:])
findSolution(n,matrix)

# findSolution(n,matrix)
# cProfile.run('findSolution(n,matrix)')