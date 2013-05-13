import numpy

class SpacePoint:
	def __init__(self):
		self.position = numpy.zeros(shape=(1,4))
		self.covariance = numpy.zeros(shape=(4,4))
		self.digits = []
		self.fake = [False]

	def addFake(self):
		if len(self.fake) == 1:
			self.fake = []
		self.fake.append(True)

	def addUseful(self):
		self.fake.append(False)

	def isFake(self):
		if False not in self.fake:
			return True

	def setPosition(self, x, y, z):
		self.position[0][0] = x
		self.position[0][1] = y
		self.position[0][2] = z

	def setTime(self, t):
		self.position[0][3] = t

	def makeFromDigits(self, xDigit, yDigit):
		self.setPosition(xDigit.x, yDigit.y, (xDigit.z + yDigit.z)/2.0)	
		self.pe = xDigit.pe + yDigit.pe
		self.time = (xDigit.t + yDigit.t)/2.0
		self.plane = xDigit.plane
		self.digits.append(xDigit)
		self.digits.append(yDigit)
		# Need to add covariances here

	def __getattr__(self, key):
		if key == "x":
			return self.position[0][0]
		elif key == "y":
			return self.position[0][1]
		elif key == "z":
			return self.position[0][2]
		elif key == "t":
			return self.position[0][3]
		else:
			raise AttributeError
