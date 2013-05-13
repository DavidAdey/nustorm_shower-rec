import Digit
import SpacePoint


class Event(object):
	def __init__(self):
		self.reconstructedVariables = {}
		self.states = []
		self.interactionType = ""
		self.nuEnergy = 0.0
		self.totalPE = 0.0
		self.current = -1
		self.coneAngle = 0.0
		self.vertexX = 0.0
		self.vertexY = 0.0
		self.vertexZ = 0.0
		self.digits = []
		self.planes = []
		self.spacePoints = []
		self.cones = []
		self.sheets = []
		self.showers = []
		self.particles = []

	def calculateTotalCharge(self, limit):
		peSum = 0.0
		for digit in self.digits:
			#digit = self.digits[d]
			peSum += digit.pe
			self.totalPE = peSum

