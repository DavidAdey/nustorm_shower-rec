import ROOT

class EventParameters(object):
	def __init__(self):
		self.meanPE = -1.0
		self.totalPlanes = -1
		self.totalPE = -1.0

	

class ParameterCalculator(object):
	def __init__(self):
		pass

	def processEvent(self, event):
		totalPE = 0.0
		allDigitX = ROOT.TH1F("allDigitX","allDigitX",1000,-5000,5000)
		allDigitY = ROOT.TH1F("allDigitY","allDigitY",1000,-5000,5000)
		
		allDigitXw = ROOT.TH1F("allDigitXw","allDigitXw",1000,-5000,5000)
		allDigitYw = ROOT.TH1F("allDigitYw","allDigitYw",1000,-5000,5000)
		for digit in event.digits:
			totalPE += digit.pe
			if (digit.view == "X"):
				allDigitX.Fill(digit.x)
				allDigitXw.Fill(digit.x, digit.pe)
			else:
				allDigitY.Fill(digit.y)
				allDigitYw.Fill(digit.y, digit.pe)
		xVar = allDigitX.GetRMS()
		yVar = allDigitY.GetRMS()	
		xVarw = allDigitXw.GetRMS()
		yVarw = allDigitYw.GetRMS()
		meanPE = totalPE / len(event.digits)
		recNuE = totalPE / 80.0
		totalPlanes = len(event.planes)
		sortedDigits = sorted(event.digits)
		firstHalf = sortedDigits[:len(sortedDigits)/2]
		secondHalf = sortedDigits[len(sortedDigits)/2:]
		firstSum = 0.0
		secondSum = 0.0
		missing = 0
		consecutive = 0
		planeKeys = sorted(event.planes.keys())
		for p in range(1,len(event.planes)-1):
			if missing > 2:
				break
			print event.planes[event.planes.keys()[p]]["X"].planeNumber
			print event.planes[event.planes.keys()[p-1]]["X"].planeNumber
			if ((event.planes[event.planes.keys()[p]]["X"].planeNumber) != (event.planes[event.planes.keys()[p-1]]["X"].planeNumber + 1)):
				missing += 1
			else:
				consecutive += 1
		for i in range(len(firstHalf)):
			firstSum += firstHalf[i].pe
		for j in range(len(secondHalf)):
			secondSum += secondHalf[j].pe
		try:
			deVariation = (secondSum/firstSum)
		except:
			deVariation = -1.0
		parameters = {"current":event.current,"meanPE":meanPE, "totalPlanes":totalPlanes, "totalPE":totalPE,"xVar":xVar,"yVar":yVar, "xVarw":xVarw, "yVarw":yVarw, "deVariation":deVariation,"consecutivePlanes":consecutive}
		return parameters

	def processCone(self):
		pass
