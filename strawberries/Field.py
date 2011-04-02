

class Field:
	
	_presentChar = '@'
	_field = []
	_maxX = 0
	_maxY = 0
	
	def getCoords(self):
		return self._field
	
	def createField(self, string):
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
	
	def __init__(self, x, y):
		self.x = x
		self.y = y