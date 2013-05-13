import Digit
import array
import ROOT
import math
import Globals

class ConeFinder(object):
	def __init__(self):
		self.coneDensity = -2.0
		self.angle = -2.0
		self.direction = {"theta":0.0,"phi":0.0}
		self.minimumFraction = 0.5
		self.vertex = {"X":0.0,"Y":0.0,"Z":0.0}
		self.chargeCaptured = {}
		self.totalFraction = 0.0

	def process(self, event):
		if (len(event.digits) < 10):
			return
		self.getConeDirection(event)
		digitRange = 1000
		if (len(event.digits) < 1000):
			digitRange = len(event.digits)
		event.calculateTotalCharge(digitRange)
		#self.chargeCaptured = self.directedCylinderDensity(event)
		self.chargeCaptured = self.cylinderDensity(event)
		"""for angleStepNo in range(int(100*(math.pi))):
			angleStep = angleStepNo / 100.0
			##print "STEP " + str(angleStep)
			enclosedCharge = self.calculateEnclosedCharge(angleStep,event.digits, digitRange)
			fraction = (enclosedCharge / event.totalPE)
			##print "FRACTION = " + str(fraction)
			if (fraction > self.minimumFraction):
				self.angle = angleStep
				return
		"""

	def directedCylinderDensity(self, event):
		chargeCaptured = {}
		for planeNo in range(-Globals.RADLENGTHPLANE,Globals.RADLENGTHPLANE):
			chargeCaptured[planeNo] = 0.0
			currentPlaneNo = self.vertex["Plane"] - planeNo
			showerCentre = self.extrapolateShower(planeNo)
			try:
				event.sheets[currentPlaneNo].extrapolation = showerCentre	
			except:
				pass
			for digit in event.digits:
				if ((digit.plane == currentPlaneNo) and (digit.view == "X") and (math.fabs(digit.x - showerCentre["X"]) < Globals.MOLIERESTEEL)):
					chargeCaptured[planeNo] += digit.pe	
				elif ((digit.plane == currentPlaneNo) and (digit.view == "Y") and (math.fabs(digit.x - showerCentre["Y"]) < Globals.MOLIERESTEEL)):
					chargeCaptured[planeNo] += digit.pe
		for key in chargeCaptured:
			chargeCaptured[key] /= event.totalPE	
		self.totalFraction = 0.0
		for key in chargeCaptured:
			self.totalFraction += chargeCaptured[key]
		
		#if totalFraction > 1.0:
		#	print "TOO MUCH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		return chargeCaptured

	def extrapolateShower(self, planeNo):
		dz = (planeNo*Globals.PLANEDEPTH)
		dx = dz*math.tan(self.direction["theta"])
		dy = dz*math.tan(self.direction["phi"])
		return {"X":(self.vertex["X"] - dx), "Y":(self.vertex["Y"] - dy), "Z":(self.vertex["Z"] - dz)}

	def cylinderDensity(self, event):
		orderedDigits = sorted(event.digits)
		orderedDigits.reverse()
		for lDigit in orderedDigits:
			#print "PE "
			#print lDigit.pe
			if lDigit.view == "X":
				largestXDigit = lDigit
				break	
		for lDigit in orderedDigits:	
			if lDigit.view == "Y":
				largestYDigit = lDigit
				break
		#print largestXDigit.pe
		try:
			good = (largestXDigit and largestYDigit)	
		except:
			return
		cx = largestXDigit.x
		cy = largestYDigit.y
		cz = largestXDigit.z
		cpx = largestXDigit.plane
		cpy = largestYDigit.plane
		"""self.vertex["X"] = cx
		self.vertex["Y"] = cy
		self.vertex["Z"] = cz	
		event.vertexX = self.vertex["X"]
		event.vertexY = self.vertex["Y"]
		event.vertexZ = self.vertex["Z"]"""
		enclosedCharge = 0.0#(largestXDigit.pe + largestYDigit.pe)
		totalSteps = 0.0
		for stepT in range(50):	
			for step in range(0,100):
				totalSteps += 1.0
				for digit in event.digits:
					currentPlaneNo = digit.plane
					planeNo = digit.plane - cpx	
					if ((digit.plane == (cpx + step)) and (digit.view == "X")):
						if ((math.fabs(digit.x - cx)) < (stepT*Globals.CHANNELWIDTH)):
							enclosedCharge += digit.pe
							if (enclosedCharge / event.totalPE) > self.minimumFraction:	
								break
					
			for step in range(0,100):
				totalSteps += 1.0
				for digit in event.digits:		
					currentPlaneNo = digit.plane
					planeNo = digit.plane - cpy	
					if ((digit.plane == (cpy + step)) and (digit.view == "Y")):
						if ((math.fabs(digit.y - cy)) < (stepT*Globals.CHANNELWIDTH)):
							enclosedCharge += digit.pe	
							if (enclosedCharge / event.totalPE) > self.minimumFraction:	
								break
		
			for step in range(1,100):
				totalSteps += 1.0
				for digit in event.digits:	
					currentPlaneNo = digit.plane
					planeNo = digit.plane - cpx
					if ((digit.plane == (cpx - step)) and (digit.view == "X")):
						if ((math.fabs(digit.x - cx)) < (stepT*Globals.CHANNELWIDTH)):
							enclosedCharge += digit.pe
							if (enclosedCharge / event.totalPE) > self.minimumFraction:	
								break
			for step in range(1,100):
				totalSteps += 1.0
				for digit in event.digits:	
					currentPlaneNo = digit.plane
					planeNo = digit.plane - cpy
					if ((digit.plane == (cpy - step)) and (digit.view == "Y")):
						if ((math.fabs(digit.y - cy)) < (stepT*Globals.CHANNELWIDTH)):
							enclosedCharge += digit.pe	
							if (enclosedCharge / event.totalPE) > self.minimumFraction:	
								break
		
		fraction = (enclosedCharge / event.totalPE)	
		if (fraction > self.minimumFraction):
			self.angle =  enclosedCharge / (totalSteps * Globals.CHANNELWIDTH * Globals.CHANNELWIDTH * Globals.PLANEDEPTH)
		else:
			self.angle = -1.0

	def getRange(self, angleStep, z):
		ranges = {}
		##print "Z"
		##print z, self.vertex["Z"]
		z = (z - self.vertex["Z"])
		coneZ = z / (math.cos(self.direction["theta"])*math.cos(self.direction["phi"]))
		vertexXOffset = self.vertex["X"] + z*math.tan(self.direction["theta"])
		vertexYOffset = self.vertex["Y"] + z*math.tan(self.direction["phi"])

		## X - THETA
		if (self.direction["theta"] > 0.0):
			if (self.direction["theta"] > angleStep):
				innerXWidth = self.vertex["X"] + z*math.tan(self.direction["theta"] - angleStep)
				outerXWidth = self.vertex["X"] + z*math.tan(self.direction["theta"] + angleStep)
			else:
				innerXWidth = self.vertex["X"] - z*math.tan(angleStep - self.direction["theta"])
				outerXWidth = self.vertex["X"] + z*math.tan(self.direction["theta"] + angleStep)
		else:
			if (self.direction["theta"] > angleStep):	
				innerXWidth = self.vertex["X"] - z*math.tan(self.direction["theta"] - angleStep)
				outerXWidth = self.vertex["X"] - z*math.tan(self.direction["theta"] + angleStep)
			else:	
				innerXWidth = self.vertex["X"] + z*math.tan(angleStep - self.direction["theta"])
				outerXWidth = self.vertex["X"] - z*math.tan(self.direction["theta"] + angleStep)
		## Y - PHI
		if (self.direction["phi"] > 0.0):
			if (self.direction["phi"] > angleStep):
				innerYWidth = self.vertex["Y"] + z*math.tan(self.direction["phi"] - angleStep)
				outerYWidth = self.vertex["Y"] + z*math.tan(self.direction["phi"] + angleStep)
			else:
				innerYWidth = self.vertex["Y"] - z*math.tan(angleStep - self.direction["phi"])
				outerYWidth = self.vertex["Y"] + z*math.tan(self.direction["phi"] + angleStep)
		else:
			if (self.direction["phi"] > angleStep):	
				innerYWidth = self.vertex["Y"] - z*math.tan(self.direction["phi"] - angleStep)
				outerYWidth = self.vertex["Y"] - z*math.tan(self.direction["phi"] + angleStep)
			else:	
				innerYWidth = self.vertex["Y"] + z*math.tan(angleStep - self.direction["phi"])
				outerYWidth = self.vertex["Y"] - z*math.tan(self.direction["phi"] + angleStep)

		########################################

		if (outerXWidth < innerXWidth):
			ranges["xMin"] = outerXWidth
			ranges["xMax"] = innerXWidth
		else:
			ranges["xMax"] = outerXWidth
			ranges["xMin"] = innerXWidth
		if (outerYWidth < innerYWidth):
			ranges["yMin"] = outerYWidth
			ranges["yMax"] = innerYWidth
		else:
			ranges["yMax"] = outerYWidth
			ranges["yMin"] = innerYWidth
		####print ranges
		return ranges
	
	def calculateEnclosedCharge(self, angleStep, digits, digitRange):
		enclosedCharge = 0.0
		limit = digitRange
		#if (len(digits) < 15):
		#	limit = len(digits)
		for d in range(0,limit):
			digit = digits[d]
			positionRange = self.getRange(angleStep, digit.z)	
			if (digit.view == "X"):
				##print digit.getRelevant(), positionRange["xMin"], positionRange["xMax"]
				if (digit.getRelevant() > positionRange["xMin"]) and (digit.getRelevant() < positionRange["xMax"]):
					enclosedCharge += digit.pe 
					###print "inside"
			if (digit.view == "Y"):
				if (digit.getRelevant() > positionRange["yMin"]) and (digit.getRelevant() < positionRange["yMax"]):
					enclosedCharge += digit.pe
		return enclosedCharge

	def calculateEnclosedCylinderCharge(self, radius, digits, digitRange):
		enclosedCharge = 0.0
		for d in range(0, digitRange):
			dpos = 0.0
			digit = digits[d]	
			if (digit.view == "X"):
				dpos = digit.x - self.vertex["X"]
			if (digit.view == "Y"):
				dpos = digit.y - self.vertex["Y"]	
			if ((dpos*dpos) < (radius*radius)):
				enclosedCharge += digit.pe
		return enclosedCharge

	def calculateEnclosedPointCharge(self, angleStep, points):
		enclosedCharge = 0.0
		for point in points:
			radius = (getattr(point,"z")*Globals.PLANEDEPTH - self.vertex["Z"])*math.tan(angleStep)
			px = getattr(point,"x")
			py = getattr(point,"y")
			if ((px*px + py*py) < (radius*radius)):
				enclosedCharge += point.pe
		return enclosedCharge

	def processDigits(self, digits):
		pass

	def getConeDirection(self, event):
		if (len(event.digits) == 0):
			return 0
		self.sheetXMeans = array.array('f')
		self.sheetYMeans = array.array('f')
		self.sheetZMeans = array.array('f')
		"""for digit in sorted(event.digits):
			if digit.view == "X":
				self.vertex["X"] = digit.x
				self.vertex["Z"] = digit.z
				break
			
		for digit in sorted(event.digits):
			##print digit.z
			if digit.view == "Y":
				##print "CHOSE THIS ONE"
				self.vertex["Y"] = digit.y
				break"""
		sortedKeys = sorted(event.sheets.keys())
		sortedSheets = sorted(event.sheets.values())
		sortedSheets.reverse()
		for s in range(len(sortedSheets)):
			if (sortedSheets[s].paired):
				self.vertex["X"] = sortedSheets[0].xMean
				self.vertex["Y"] = sortedSheets[0].yMean
				self.vertex["Z"] = sortedSheets[0].z
				self.vertex["Plane"] = sortedSheets[0].planeNumber
				break
		event.vertexX = self.vertex["X"]
		event.vertexY = self.vertex["Y"]
		event.vertexZ = self.vertex["Z"]
		##print "NOW"
		#for digit in event.digits:
			##print self.vertex["X"], digit.x, self.vertex["Y"], digit.y, self.vertex["Z"], digit.z
		
		for sheet in event.sheets:
			#if math.fabs(event.sheets[sheet].planeNumber - self.vertex["Plane"]) < 5:
			if (event.sheets[sheet].paired == True):
				self.sheetXMeans.append(event.sheets[sheet].xMean)
				self.sheetYMeans.append(event.sheets[sheet].yMean)
				self.sheetZMeans.append(event.sheets[sheet].z)
		self.coneXDirectionGraph = ROOT.TGraph(len(self.sheetXMeans),self.sheetZMeans,self.sheetXMeans)
		self.coneYDirectionGraph = ROOT.TGraph(len(self.sheetYMeans),self.sheetZMeans,self.sheetYMeans)
		self.coneXDirectionGraph.Fit("pol1")
		self.coneYDirectionGraph.Fit("pol1")
		xFunction = self.coneXDirectionGraph.GetFunction("pol1")
		yFunction = self.coneYDirectionGraph.GetFunction("pol1")
		xGradient = xFunction.GetParameter(1)
		yGradient = yFunction.GetParameter(1)
		self.direction["theta"] = math.atan(xGradient)
		self.direction["phi"] = math.atan(yGradient)
