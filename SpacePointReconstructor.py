import SpacePoint
import math

class SpacePointReconstructor(object):
	def __init__(self):
		self.algorithms = {"sort":self.sortDigits, "makeAllPoints":self.makeAllPoints}
		self.spacePoints = []

	def makeSpacePoints(self, event, algorithm="makeAllPoints"):
		digits = event.digits
		self.algorithms["sort"](digits)
		self.algorithms[algorithm]()
		event.spacePoints = self.spacePoints

	def sortDigits(self, digits):
		print str(len(digits)) + "digits to sort"
		self.planes = {}
		for digit in digits:
			if digit.plane not in self.planes:
				self.planes[digit.plane] = {'X':[], 'Y':[]}
				self.planes[digit.plane][digit.view].append(digit)
			else:
				self.planes[digit.plane][digit.view].append(digit)	

	def makeAllPoints(self):
		for key in self.planes:
			plane = self.planes[key]
			for xDigit in plane['X']:
				for yDigit in plane['Y']:
					if math.fabs(xDigit.t - yDigit.t) < 1.0:
						#print "passed cut"
						newPoint = SpacePoint.SpacePoint()
						newPoint.makeFromDigits(xDigit, yDigit)
						self.spacePoints.append(newPoint)


	def getPoints(self):
		return self.spacePoints
