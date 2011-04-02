
class ComboCache:

	cache = {}

	def clear(self):
		self.cache = {}
		
	def isPresent(self, solution):
		greenhouses = solution.getGreenhouses()
		
		currentCache = self.cache
		for greenhouse in greenhouses:
			if (not greenhouse in currentCache):
				return False
			else:
				currentCache = currentCache[greenhouse]
				
		return True
		
	def insert(self, solution):
		greenhouses = solution.getGreenhouses()
		
		currentCache = self.cache
		for greenhouse in greenhouses:
			if (not greenhouse in currentCache):
				currentCache[greenhouse] = {}
				
			currentCache = currentCache[greenhouse]
			