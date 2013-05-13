import Plane
import Digit

class PlaneReconstructor(object):
	def __init__(self):
		self.planes = {}

	def sortDigits(self, event):
		for digit in event.digits:
			if digit.plane not in self.planes:
				self.planes[digit.plane] = {"X":Plane.Plane(digit.plane,"X"), "Y":Plane.Plane(digit.plane,"Y")}
				self.planes[digit.plane][digit.view].digits.append(digit)
			else:
				self.planes[digit.plane][digit.view].digits.append(digit)

	def calculateVariables(self):
		for plane in self.planes:	
			self.planes[plane]["Y"].calculateVariables()
			self.planes[plane]["X"].calculateVariables()
	def getPlanes(self):
		return self.planes
