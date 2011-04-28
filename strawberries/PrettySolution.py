from Field import FieldSquare
import math
class PrettySolution:

	clusters = []
	
	def getCost(self):
		cost = 0
		for cluster in self.clusters:
			cost = cost + cluster.getCost()
		cost = cost + 10 * len(self.clusters)
		return cost
	
	def getNewClusterCenters(self):
		centers = []
		for cluster in self.clusters:
			centers.append(cluster.getNewCenter())
			
		return centers
	
	def addPointToCluster(self, point):
		min = 0
		currentCluster = None
		for cluster in self.clusters:
			metric = cluster.costToAdd(point)
			if (currentCluster == None or metric < min):
				min = metric
				currentCluster = cluster
		currentCluster.addPointToCluster(point)
		
	def printSolution(self,maxX,maxY):
		for y in range(maxY):
			for x in range(maxX):
				square = FieldSquare(x,y)
				rep = "."
				for cluster in self.clusters:
					if cluster.containsPoint(square):
						rep = cluster.index
				print(rep,end='')
			print("\n",end='')

	def __eq__(self, obj):
		if (obj == None):
			return False
		for cluster1 in self.clusters:
			contains = False
			for cluster2 in obj.clusters:
				contains = contains or cluster1 == cluster2
			if (not contains):
				return False
				
		return True
		
	def __init__(self, clusterPoints):
		index = 0
		self.clusters = []
		for point in clusterPoints:
			self.clusters.append(Cluster(point,index))
			#print(str(index) + ": " + point.printSquare())
			index = index + 1
	
class Cluster:
	
	_center = None
	_pointCollection = []
	index = 0
	minX = 0
	minY = 0
	maxX = 0
	maxY = 0
	
	def getCost(self):
		if (self.minX == None):
			return 0
		return (self.maxX-self.minX)*(self.maxY-self.minY)
	
	def distanceFromCenter(self,point):
		return math.sqrt(pow(point.x-self._center.x,2) + pow(point.y-self._center.y,2))
		
	def costToAdd(self,point):
		minX = self.minX
		minY = self.minY
		maxX = self.maxX
		maxY = self.maxY
		if minX == None or point.x < minX:
			minX = point.x
		if maxX == None or point.x > maxX:
			maxX = point.x
		if minY == None or point.y < minY:
			minY = point.y
		if maxY == None or point.y > maxY:
			maxY = point.y	

		newCost = (maxX-minX)*(maxY-minY)
		oldCost = self.getCost()
		
		return newCost - oldCost
		
	def addPointToCluster(self, point):
		if self.minX == None or point.x < self.minX:
			self.minX = point.x
		if self.maxX == None or point.x > self.maxX:
			self.maxX = point.x
		if self.minY == None or point.y < self.minY:
			self.minY = point.y
		if self.maxY == None or point.y > self.maxY:
			self.maxY = point.y	
		self._pointCollection.append(point)
		
	def containsPoint(self,newPoint):
		for point in self._pointCollection:
			if newPoint == point:
				return True
		return False
		
	def getNewCenter(self):
		if (len(self._pointCollection)==0):
			return self._center
		sumX = 0
		sumY = 0
		for point in self._pointCollection:
			sumX = sumX + point.x
			sumY = sumY + point.y
		newCenter = FieldSquare(sumX/len(self._pointCollection), sumY/len(self._pointCollection))
		return newCenter
		
	def __eq__(self, obj):
		if (obj == None):
			return False
		return self._center == obj._center
	
	def __init__(self,point,index):
		self._center = point
		self.index = index
		self._pointCollection = []
		self.minX = point.x
		self.minY = point.y
		self.maxX = point.x
		self.maxY = point.y
		