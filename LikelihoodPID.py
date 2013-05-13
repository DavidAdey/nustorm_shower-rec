import math
import ROOT
import Globals

class LikelihoodPID(object):
	def __init__(self):
		self.ratios = {}

	def loadLikelihoods(self, ratioFile):
		rFile = ROOT.TFile(ratioFile,'r')
		ratioHistogram = ROOT.gDirectory.Get("cc")
		self.certain = ratioHistogram.GetMean()
		for binNo in range(ratioHistogram.GetNbinsX()):
			ratio = ratioHistogram.GetBinContent(binNo)
			density = ratioHistogram.GetBinCenter(binNo)
			self.ratios[density] = (ratio)

	def PID(self, event):
		ratio = self.getRatio(event.reconstructedVariables["coneDensity"])
		if ((event.reconstructedVariables["coneDensity"] > self.certain) and (ratio == 0.0)):
			pid = 1
			error = 0.0
			return {"pid":pid, "error":error}
		elif (ratio == 0.0):
			pid = 0
			error = 0.0
			return {"pid":pid, "error":error}
		else:
			print ratio
			ratio = math.log(ratio)
		if (ratio > 1.0):
			pid = 1
			error = 0.0#math.sqrt(ratio)
		else:
			pid = 0
			error = 0.0#math.sqrt(ratio)
		return {"pid":pid, "error":error}

	def getRatio(self, density):
		closestDensities = {}
		for densityKey in self.ratios:
			dDensity = math.fabs(density - densityKey)
			ratio = self.ratios[densityKey]
			closestDensities[dDensity] = densityKey
		sortedDensityKeys = sorted(closestDensities.keys())
		ratio = self.ratios[closestDensities[sortedDensityKeys[0]]]
		return ratio
