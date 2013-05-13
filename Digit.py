import Globals
class Digit(object):
	def __init__(self, event, x, y, t, pe, plane, view, intType):
		self.interactionType = intType
		self.event = event
		self.x = x
		self.y = y
		self.pe = pe
		self.t = t
		self.plane = plane
		self.view = view
		self.z = (plane * Globals.PLANEDEPTH)
	def __lt__(self, other):
		return (self.pe < other.pe)
			
	def getRelevant(self):
		if self.view == "Y":
			return self.y
		else:
			return self.x	
