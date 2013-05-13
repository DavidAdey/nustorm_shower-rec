import Globals
import numpy

class Sheet(object):
	def __init__(self):
		self.z = 0.0
		self.points = []
		self.planes = []
		self.xMean = 0.0
		self.yMean = 0.0
		self.covariance = numpy.zeros(shape=(2,2))
		self.event = 0
		self.planeNumber = 0.0
		self.totalPE = 0.0
		self.hasX = False
		self.hasY = False
		self.extrapolation = {"X":0.0,"Y":0.0,"Z":0.0}

	def merge(self):
		self.event = self.planes[0].event
		zSum = 0.0
		planeSum = 0.0	
		for plane in self.planes:
			#plane.findTrackHits()
#			plane.calculateVariables()
			#zSum += plane.z
			self.totalPE += plane.totalPE
			planeSum += float(plane.planeNumber)
			if plane.view == "X":
				self.xMean = plane.mean	
				self.covariance[0][0] = plane.variance
				self.hasX = True
			elif plane.view == "Y":
				self.yMean = plane.mean
				self.covariance[1][1] = plane.variance
				self.hasY = True
		#self.z = zSum / len(self.planes)
		self.paired = (self.hasX and self.hasY)
		self.planeNumber = planeSum / len(self.planes)
		self.z = self.planeNumber * Globals.PLANEDEPTH
		#print self.planeNumber, self.xMean
				
	def __lt__(self, other):
		return (self.totalPE < other.totalPE)

	def __gt__(self, other):
		return (self.totalPE > other.totalPE)
