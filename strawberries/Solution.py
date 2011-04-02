
from functools import reduce
from Field import FieldSquare

class Solution:

	_areaCost = 1
	_greenhouseCost = 10
	_problem = None
	_cost = 0
	_remaining = []
	_greenhouses = []
	maxGreenhouses = 0
	
	def getGreenhouses(self):
		return self._greenhouses
		
	def setGreenhouses(self, greenhouses):
		self._greenhouses = greenhouses
	
	def printSolution(self):
		i = 1
		for greenhouse in self._greenhouses:
			greenhouse.index = i
			i += 1
			
		print(self.computeCost())
		for y in range(self._problem.getMaxY()):
			for x in range(self._problem.getMaxX()):
				inHouse = False
				for greenhouse in self._greenhouses:
					if (greenhouse.containsCoord(x,y)):
						inHouse = True
						print(greenhouse.index,end='')
						break
				if (not inHouse):
					print('0',end='')
			print('\n',end='')
	
	def getNumberOfGreenhouses(self):
		return len(self._greenhouses)
	
	def setState(self, solution):
		self._remaining = list(solution._remaining)
		self._greenhouses = list(solution._greenhouses)
		self.maxGreenhouses = solution.maxGreenhouses
	
	def computeCost(self):
		totalGreenhouseCost = self._greenhouseCost * len(self._greenhouses)
		totalAreaCost = 0
		for x in self._greenhouses:
			totalAreaCost += x.getArea()*self._areaCost
		return totalGreenhouseCost + totalAreaCost
		
	def getRemaining(self):
		return self._remaining
		
	def placeGreenhouse(self, left, right, top, bottom):
		greenhouse = Greenhouse(left,right,top,bottom)
		
		if (self.willOverlap(greenhouse)):
			return False
		else:
			
			stillNotCovered = []
			covered = 0
			for coord in self._remaining:
				if (not greenhouse.containsCoord(coord.x,coord.y)):
					stillNotCovered.append(coord)
				else:
					covered += 1
			
			if (self.maxGreenhouses - len(self._greenhouses) >=2 and
				self.maxGreenhouses - len(self._greenhouses) - 1 < len(stillNotCovered)):
				if ((greenhouse.getArea()) - covered > self._greenhouseCost):
					return False
					
			self._remaining = stillNotCovered
			self._greenhouses.append(greenhouse)
			self._rearrange()
			return True
		
	def willOverlap(self, greenhouse):
		overlaps = False
		for existingGreenhouse in self._greenhouses:
			overlaps = overlaps or existingGreenhouse.overlaps(greenhouse)
			
		return overlaps
			
	def placeFinalGreenhouse(self):
		if (len(self._remaining) == 0):
			return False
		left = self._remaining[0].x
		right = self._remaining[0].x
		top = self._remaining[0].y
		bottom = self._remaining[0].y
		for coord in self._remaining:
			if coord.x < left:
				left = coord.x
			if coord.x > right:
				right = coord.x
			if coord.y < top:
				top = coord.y
			if coord.y > bottom:
				bottom = coord.y
				
		return self.placeGreenhouse(left,right,top,bottom)
		
	def _rearrange(self):
		sorted(self._greenhouses, key=Greenhouse.getLeft ) 
		sorted(self._greenhouses, key=Greenhouse.getTop )
		sorted(self._greenhouses, key=Greenhouse.getRight )
		sorted(self._greenhouses, key=Greenhouse.getBottom )
		
	def isEqual(self, solution):
		if (solution.getNumberOfGreenhouses() == self.getNumberOfGreenhouses()):
			self.rearrange()
			solution.rearrange()
			for i in range(self.getNumberOfGreenhouses()):
				if (not self._greenhouses[i].__eq__(solution._greenhouses[i])):
					return False
			return True
		else:
			return False
		
	def __init__(self, problem):
		self._problem = problem
		self._remaining = list(problem.getCoords())
		self._greenhouses = []
			
class Greenhouse:

	_left = 0
	_top = 0
	_right = 0
	_bottom = 0
	index = 0
	_corners = []
	_printedRepresentation = ""
	_containedCoordinates = []
	
	def addContainedCoordinate(self,coord):
		self._containedCoordinates.append(coord)
		
	def getNumberOfContainedCoordinates(self):
		return len(self._containedCoordinates)
		
	def getWastedCoordinates(self):
		return self.getArea() - self.getNumberOfContainedCoordinates()
	
	def getLeft(self):
		return self._left
	def getRight(self):
		return self._right
	def getTop(self):
		return self._top
	def getBottom(self):
		return self._bottom
	
	def sortsAbove(self, greenhouse):
		compareLeft = self.compare(self._left, greenhouse._left)
		if (compareLeft == 0):
			compareTop = self.compare(self._top, greenhouse._top)
			if (compareTop == 0):
				compareRight = self.compare(self._right, greenhouse._right)
				if (compareRight == 0):
					return self.compare(self._bottom,greenhouse._bottom)
				else:
					return compareRight
			else:
				return compareTop
		else:
			return compareLeft
			
	def compare(self, a, b):
		if (a < b): return 1
		if (b < a): return -1
		else: return 0
	
	def __eq__(self, greenhouse):
		return (self._left == greenhouse._left and
				self._right == greenhouse._right and
				self._top == greenhouse._top and
				self._bottom == greenhouse._bottom)
				
	def __hash__(self):
		return self._printedRepresentation.__hash__()
	
	def getArea(self):
		return (self._right - self._left + 1) * (self._bottom - self._top + 1)
		
	def getCorners(self):
		return self._corners
		
	def overlaps(self, greenhouse):
		containsCorner = False
		for corner in greenhouse.getCorners():
			containsCorner = containsCorner or self.containsCoord(corner.x,corner.y)
		for corner in self.getCorners():
			containsCorner = containsCorner or greenhouse.containsCoord(corner.x,corner.y)
		return containsCorner
		
	def containsCoord(self, x, y):
		return (x >= self._left and x <= self._right and
				y >= self._top and y <= self._bottom)

	def printGreenhouse(self):
		return '(%(left)s,%(right)s,%(top)s,%(bottom)s)' % \
				{'top':self._top,'left':self._left,'bottom':self._bottom,'right':self._right}
				
	def __init__(self, left, right, top, bottom):
		self._left = min(left,right)
		self._right = max(left,right)
		self._top = min(top,bottom)
		self._bottom = max(top,bottom)
		corners = []
		corners.append(FieldSquare(self._left,self._top))
		corners.append(FieldSquare(self._left,self._bottom))
		corners.append(FieldSquare(self._right,self._top))
		corners.append(FieldSquare(self._right,self._bottom))		
		self._corners = corners
		self._printedRepresentation = self.printGreenhouse()