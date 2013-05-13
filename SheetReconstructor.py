import Sheet
import Helpers

class SheetReconstructor(object):
	def __init__(self):
		self.algorithms = {}
		self.sheets = {}

	def makeFromPlanes(self, event):
		for planeKey in event.planes:
			planeNo = event.planes[planeKey]
			for view in ['X','Y']:
				plane = planeNo[view]
				if plane.planeNumber not in self.sheets:
					self.sheets[plane.planeNumber] = Sheet.Sheet()
					self.sheets[plane.planeNumber].planes.append(plane)
				else:
					self.sheets[plane.planeNumber].planes.append(plane)
		self.sortSheets()

	def mergeAll(self):
		for sheet in self.sheets:
			self.sheets[sheet].merge()

	def sortPoints(self, event):
		for point in event.spacePoints:
			if point.plane not in self.sheets:
				self.sheets[point.plane] = Sheet.Sheet()
				self.sheets[point.plane].points.append(point)
			else:
				self.sheets[point.plane].points.append(point)

	def sortSheets(self):
		keys = self.sheets.keys()
		keys.sort()
		#print keys
		self.sortedSheets = [self.sheets[key] for key in keys]

	def filterPoints(self, event):
		self.sortSheets()
		for sheetNo in range(len(self.sortedSheets) - 1):
			sheet = self.sortedSheets[sheetNo]
			trailingSheet = self.sortedSheets[sheetNo + 1]
			for pointA in self.sortedSheets[sheetNo].points:
				for pointBNo in range(len(self.sortedSheets[sheetNo+1].points)):
					if not (pointA.isFake() and self.sortedSheets[sheetNo+1].points[pointBNo].isFake()):
						if (Helpers.chi2(pointA, self.sortedSheets[sheetNo+1].points[pointBNo]) > 10000.0):
							self.sortedSheets[sheetNo+1].points[pointBNo].addFake()
						else:
							self.sortedSheets[sheetNo+1].points[pointBNo].addUseful()	
						#print "deleted, now"
							#print len(self.sortedSheets[sheetNo + 1].points)
		event.spacePoints = []
		for sheet in self.sortedSheets:
			for point in sheet.points:
				if not point.isFake():
					event.spacePoints.append(point)
		return event

	def getSheets(self):
		return self.sheets

	def divideSheet(self, sheet):
		return []

	def divideSheets(self):
		for sheet in self.planes:
			self.sheets.append(self.divideSheet(plane))
