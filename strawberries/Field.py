
import random
class Field:
	
	_presentChar = '@'
	_field = []
	_maxX = 0
	_maxY = 0
	
	def getCoords(self):
		return self._field
		
	def getRandomCoords(self, n):
		points = []
		for i in range(n):
			points.append(self._field[random.randint(0,len(self._field)-1)])
		return points
	
	def createField(self, string):
		self._field = []
		self._maxX = 0
		self._maxY = 0
		y = 0
		for line in string.split("\n"):
			x = 0
			for char in line:
				if ( char == self._presentChar ):
					self._field.append(FieldSquare(x,y))
				x += 1
			self._maxX = x
			y += 1
		self._maxY = y
		
	def printField(self):
		for y in range(self._maxY):
			for x in range(self._maxX):
				matching = list(filter( lambda square: (square.x==x and square.y==y), self._field))
				print(1 if len(matching)==1 else 0, end='')
			print("\n", end='')
			
	def getMaxX(self):
		return self._maxX
		
	def getMaxY(self):
		return self._maxY
		
class FieldSquare:

	x = 0
	y = 0
	
	def printSquare(self):
		return str(self.x) + " " + str(self.y)
	
	def __eq__(self, obj):
		return self.x == obj.x and self.y == obj.y
	
	def __init__(self, x, y):
		self.x = x
		self.y = y