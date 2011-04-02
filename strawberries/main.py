
from Field import Field
from Solution import Solution
from queue import Queue
from ComboCache import ComboCache
import cProfile

matrix = ("..@@@@@...............\n" +
			"..@@@@@@........@@@...\n" +
			".....@@@@@......@@@...\n" + 
			".......@@@@@@@@@@@@...\n" +
			".........@@@@@........\n" +
			".........@@@@@........" )

n = 3

def findSolution(n, matrix):
	field = Field()
	field.createField(matrix)
	field.printField()

	solutions = Queue()

	minSolution = None
	cache = ComboCache()
	preAnsweredCache = {}
	
	for j in range(1,n+1):
		preAnsweredCache[j]= []

	for i in range(1,n+1):
		cache.clear()

		if (i-2 in preAnsweredCache):
			for sol in preAnsweredCache[i-2]:
				newSolution = Solution(field)
				newSolution.setState(solution)
				newSolution.maxGreenhouses = i
				solutions.put(newSolution)
		else:
			firstSolution = Solution(field)
			firstSolution.maxGreenhouses = i
			solutions.put(firstSolution)
		
		while (not solutions.empty()):
			solution = solutions.get()
			if (minSolution == None or solution.computeCost() < minSolution.computeCost()):
				if (solution.getNumberOfGreenhouses() == (solution.maxGreenhouses-1)):
					## find the leftmost, topmost, rightmost, bottommost 
					## uncovered points. They form your final greenhouse.
					## if left < right and top < bottom (or right > right and bottom > bottom,
					## it overlaps, and no solution using this is possible.
					if (solution.placeFinalGreenhouse()):
						cost = solution.computeCost()
						if (minSolution == None or cost < minSolution.computeCost()):
							minSolution = solution
				else:
					## iterate through the remaining uncovereds, both for start
					## and end. reject overlaps!

					for corner1 in solution.getRemaining():
						for corner2 in solution.getRemaining():				
							newSolution = Solution(field)
							newSolution.setState(solution)
							if (newSolution.placeGreenhouse(corner1.x, corner2.x, corner1.y, corner2.y)):
								if (not cache.isPresent(newSolution)):
									solutions.put(newSolution)
									preAnsweredCache[newSolution.getNumberOfGreenhouses()].append(newSolution)
									cache.insert(newSolution)
						
	minSolution.printSolution()
	
cProfile.run('findSolution(n,matrix)')