

class ShowerReconstructor(object):
	def __init__(self):
		self.showerHits = {}

	def process(self, event):
		pass

	def getPlaneShowerHits(self, event):
		for plane in event.planes:
			self.showerHits[plane] = {}
			for view in ['X','Y']:
				hits = plane[view].findTrackHits()
				self.showerHits[plane][view] = hits

	def recogniseShowerPatterns(self):
		nTracks = {}
		for plane in self.showerHits:
			nTracks[plane] = {'X':0, 'Y':0}
			for view in ['X','Y']
				nTracks[plane][view] = (len(self.showerHits[plane][view]))
		for tPoint in nTracks:
			for view in ['X','Y']
				for trackNo in range(tPoint[view]):
					pass

	def fitShowerDirections(self):
		pass

		
	

