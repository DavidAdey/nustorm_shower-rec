import ROOT

class BasicCutPID(object):
	def __init__(self):
		pass
		self.ccTotalPEDisc = ROOT.TH1F("ccTotalPEDisc","ccTotalPEDisc",100,0,10000)
		self.ncTotalPEDisc = ROOT.TH1F("ncTotalPEDisc","ncTotalPEDisc",100,0,10000)
	
		self.ccXVarDisc = ROOT.TH1F("xVarDisc","xVarDisc",100,0,10000)
		self.ncYVarDisc = ROOT.TH1F("yVarDisc","yVarDisc",100,0,10000)



	def setCuts(self, meanPE = 0.0, planesHit = 0, totalPE = 0.0):
		self.meanPE = meanPE
		self.planesHit = planesHit
		self.totalPE = totalPE

	def PID(self, parameters, event):
		if (parameters["meanPE"] > self.meanPE) \
		or (parameters["totalPlanes"] > self.planesHit) \
		or (parameters["totalPE"] > self.totalPE):
			return {"guess":1, "true":event.current}
		else:
			return {"guess":0, "true":event.current}

	def caclulcateDiscPower(self,parameters):
		pass
		#for totalPE in range(10000):
		#	if parameters["totalPE"] > totalPE
