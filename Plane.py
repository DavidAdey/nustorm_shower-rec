import ROOT
import math
import Digit
import Helpers
import Globals

class Plane(object):
	def __init__(self, number, view):
		self.view = view
		self.planeNumber = number
		self.digits = []
		self.event = -1
		self.mean = 0.0
		self.variance = 0.0
		self.skewness = 0.0
		self.kurtosis = 0.0
		self.totalPE = 0.0
		self.meanDigit = 0
		self.nFoundPeaks = 0
		self.showerPoints = []

	def findTrackHits(self):
		hist = ROOT.TH1F("h","h",100,-2500.0,2500.0)
		for digit in self.digits:
			if (digit.pe > (Globals.MIP / 2.0)):
				hist.Fill(digit.getRelevant())
		spectrum = ROOT.TSpectrum()
		self.nFoundPeaks = spectrum.Search(hist,2,"", 0.0025)
		showerPoints = spectrum.GetPositionX()
		for i in range(self.nFoundPeaks):
			self.showerPoints.append(showerPoints[i])
		self.showerPoints.sort()
		#print nFoundPeaks, len(self.showerPoints),
		#print "COMPARE"
		del hist
		if self.nFoundPeaks > 0:
			return self.showerPoints
		else:
			return []

	def calculateVariables(self):
		if (len(self.digits) > 0):
			self.event = self.digits[0].event
			self.mean = self.calculateMean()
			self.variance = self.calculateVariance()
			#print self.variance
			#print "was the variance"
			self.skewness = self.calculateSkewness()
			self.kurtosis = self.calculateKurtosis()
			self.totalPE = self.calculateTotalPE()
			self.meanDigit = Helpers.findDigitNo(self.mean)

	def getVariables(self):
		return {"mean":self.mean, "variance":self.variance, "skewness":self.skewness, "kurtosis":self.kurtosis, "meanDigit":self.meanDigit}

	def calculateMean(self):
		weightedLocationSum = 0.0
		weightSum = 0.0
		wmHist = ROOT.TH1F("wmh","wmh",1000,-5000.0,5000.0)
		for digit in self.digits:	
			if (digit.view == self.view):	
				wmHist.Fill(digit.getRelevant(), digit.pe)
				weightSum += digit.pe
				weightedLocationSum += (digit.getRelevant()*digit.pe)
		##print weightedLocationSum / (float(len(self.digits)) * weightSum)
		return wmHist.GetMean()#(weightedLocationSum / (weightSum * float(len(self.digits))))
	
	def calculateVariance(self):
		#e(x^2) - e(x)^2
		weightedLocationSum = 0.0
		weightSum = 0.0
		weightedSquareLocationSum = 0.0
		for digit in self.digits:
			weightSum += digit.pe
			weightedLocationSum += (digit.getRelevant()*digit.pe)
			weightedSquareLocationSum += ((digit.getRelevant()*digit.pe)*(digit.getRelevant()*digit.pe))
		ex = (weightedLocationSum / (weightSum*float(len(self.digits))))
		ex2 = (weightedSquareLocationSum / (weightSum*weightSum*float(len(self.digits))))
		try:
			variance = math.sqrt((ex2) - (ex*ex))
		except:
			return 0.0
		return variance

	def calculateSkewness(self):
		return 0.0

	def calculateKurtosis(self):
		return 0.0

	def calculateTotalPE(self):
		self.totalPE = 0.0
		for digit in self.digits:
			self.totalPE += digit.pe
		##print self.totalPE
		return self.totalPE
