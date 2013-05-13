import ROOT
import unpack
import numpy
import array
import math

class ROOTFileManager(object):
	def __init__(self):
		#pass
		self.count = 0
		self.rootFile = ROOT.TFile("events.root","recreate")

	def setupTree(self):
		ROOT.gROOT.ProcessLine("struct TempDigit {\
					Int_t event;\
					Double_t x;\
					Double_t y;\
					Double_t z;\
					Double_t t;\
					Int_t pe;\
					Int_t plane;\
					Int_t current;\
					Int_t interactionType;\
					Int_t view;\
					};")
		ROOT.gROOT.ProcessLine("struct TempSpacePoint {\
					Int_t event;\
					Double_t x;\
					Double_t y;\
					Double_t z;\
					};")
		ROOT.gROOT.ProcessLine("struct TempPlane {\
					Int_t event;\
					Int_t view;\
					Double_t z;\
					Int_t planeNumber;\
					Double_t totalPE;\
					Double_t mean;\
					Double_t hitA;\
					Double_t variance;\
					Double_t skewness;\
					Double_t kurtosis;\
					};")
		ROOT.gROOT.ProcessLine("struct TempSheet {\
					Int_t event;\
					Double_t xMean;\
					Double_t yMean;\
					Double_t xExtrap;\
					Double_t yExtrap;\
					Double_t yWidth;\
					Double_t xWidth;\
					Double_t planeNumber;\
					};")
		ROOT.gROOT.ProcessLine("struct TempEvent {\
					Int_t event;\
					Int_t current;\
					Int_t interactionType;\
					Int_t pid;\
					Double_t totalPE;\
					Double_t nuE;\
					Double_t recE;\
					Int_t totalPlanes;\
					Double_t xVar;\
					Double_t yVar;\
					Double_t coneAngle;\
					Double_t coneDensity;\
					Double_t vertexX;\
					Double_t vertexY;\
					Double_t vertexZ;\
					};")

		self.tempEvent = ROOT.TempEvent()
		self.eventTree = ROOT.TTree("eventTree","eventTree")
		self.eventTree.Branch("nuE",ROOT.AddressOf(self.tempEvent,"nuE"),"nuE/D")	
		self.eventTree.Branch("recE",ROOT.AddressOf(self.tempEvent,"recE"),"recE/D")	
		self.eventTree.Branch("totalPE",ROOT.AddressOf(self.tempEvent,"totalPE"),"totalPE/D")
		self.eventTree.Branch("totalPlanes",ROOT.AddressOf(self.tempEvent,"totalPlanes"),"totalPlanes/I")
		self.eventTree.Branch("current",ROOT.AddressOf(self.tempEvent,"current"),"current/I")
		self.eventTree.Branch("interactionType",ROOT.AddressOf(self.tempEvent,"interactionType"),"type/I")
		self.eventTree.Branch("pid",ROOT.AddressOf(self.tempEvent,"pid"),"pid/I")	
		self.eventTree.Branch("event",ROOT.AddressOf(self.tempEvent,"event"),"event/I")
		self.eventTree.Branch("xVar",ROOT.AddressOf(self.tempEvent,"xVar"),"xVar/D")		
		self.eventTree.Branch("yVar",ROOT.AddressOf(self.tempEvent,"yVar"),"yVar/D")		
		self.eventTree.Branch("coneAngle",ROOT.AddressOf(self.tempEvent,"coneAngle"),"coneAngle/D")	
		self.eventTree.Branch("coneDensity",ROOT.AddressOf(self.tempEvent,"coneDensity"),"coneDensity/D")	
		self.eventTree.Branch("vertexx",ROOT.AddressOf(self.tempEvent,"vertexX"),"vertexx/D")		
		self.eventTree.Branch("vertexy",ROOT.AddressOf(self.tempEvent,"vertexY"),"vertexy/D")		
		self.eventTree.Branch("vertexz",ROOT.AddressOf(self.tempEvent,"vertexZ"),"vertexz/D")
		
		self.tempDigit = ROOT.TempDigit()
		self.tree = ROOT.TTree("tree","tree")
		self.tree.Branch("event",ROOT.AddressOf(self.tempDigit,"event"),"event/I")
		self.tree.Branch("current",ROOT.AddressOf(self.tempDigit,"current"),"current/I")
		self.tree.Branch("interacionType",ROOT.AddressOf(self.tempDigit,"interactionType"),"interactionType/I")
		self.tree.Branch("view",ROOT.AddressOf(self.tempDigit,"view"),"view/I")
		self.tree.Branch("x",ROOT.AddressOf(self.tempDigit,"x"),"x/D")
		self.tree.Branch("y",ROOT.AddressOf(self.tempDigit,"y"),"y/D")
		self.tree.Branch("z",ROOT.AddressOf(self.tempDigit,"z"),"z/D")
		self.tree.Branch("t",ROOT.AddressOf(self.tempDigit,"t"),"t/D")
		self.tree.Branch("pe",ROOT.AddressOf(self.tempDigit,"pe"),"pe/I")	
		self.tree.Branch("plane",ROOT.AddressOf(self.tempDigit,"plane"),"plane/I")	

		self.tempSpacePoint = ROOT.TempSpacePoint()
		self.pointTree = ROOT.TTree("points","points")
		self.pointTree.Branch("event",ROOT.AddressOf(self.tempSpacePoint,"event"),"event/I")
		self.pointTree.Branch("x",ROOT.AddressOf(self.tempSpacePoint,"x"),"x/D")
		self.pointTree.Branch("y",ROOT.AddressOf(self.tempSpacePoint,"y"),"y/D")
		self.pointTree.Branch("z",ROOT.AddressOf(self.tempSpacePoint,"z"),"z/D")
		
		self.planeTree = ROOT.TTree("planes","planes")
		self.tempPlane = ROOT.TempPlane()
		self.planeTree.Branch("z",ROOT.AddressOf(self.tempPlane,"z"),"z/D")
		self.planeTree.Branch("pe",ROOT.AddressOf(self.tempPlane,"totalPE"),"pe/D")
		self.planeTree.Branch("event",ROOT.AddressOf(self.tempPlane,"event"),"event/I")
		self.planeTree.Branch("view",ROOT.AddressOf(self.tempPlane,"view"),"view/I")
		self.planeTree.Branch("mean",ROOT.AddressOf(self.tempPlane,"mean"),"mean/D")	
		self.planeTree.Branch("hitA",ROOT.AddressOf(self.tempPlane,"hitA"),"hitA/D")	
		self.planeTree.Branch("variance",ROOT.AddressOf(self.tempPlane,"variance"),"variance/D")
		self.planeTree.Branch("plane",ROOT.AddressOf(self.tempPlane,"planeNumber"),"plane/I")
		self.planeTree.Branch("skewness",ROOT.AddressOf(self.tempPlane,"skewness"),"skewness/D")
		self.planeTree.Branch("kurtosis",ROOT.AddressOf(self.tempPlane,"kurtosis"),"kurtosis/D")
	
		self.sheetTree = ROOT.TTree("sheets","sheets")
		self.tempSheet = ROOT.TempSheet()
		self.sheetTree.Branch("xMean",ROOT.AddressOf(self.tempSheet,"xMean"),"xMean/D")
		self.sheetTree.Branch("yMean",ROOT.AddressOf(self.tempSheet,"yMean"),"yMean/D")
		
		self.sheetTree.Branch("xExtrap",ROOT.AddressOf(self.tempSheet,"xExtrap"),"xExtrap/D")
		self.sheetTree.Branch("yExtrap",ROOT.AddressOf(self.tempSheet,"yExtrap"),"yExtrap/D")
		self.sheetTree.Branch("event",ROOT.AddressOf(self.tempSheet,"event"),"event/I")
		self.sheetTree.Branch("planeNumber",ROOT.AddressOf(self.tempSheet,"planeNumber"),"planeNumber/D")

		self.ccxVarw = ROOT.TH1F("ccxvarw","ccxvarw",100,0,1000)
		self.ncxVarw = ROOT.TH1F("ncxvarw","ncxvarw",100,0,1000)
		self.ccxVar = ROOT.TH1F("ccxvar","ccxvar",100,0,1000)
		self.ncxVar = ROOT.TH1F("ncxvar","ncxvar",100,0,1000)
		self.ccTotalPE = ROOT.TH1F("cctotalpe","cctotalpe",5000,0,50000)
		self.ncTotalPE = ROOT.TH1F("nctotalpe","nctotalpe",5000,0,50000)
		self.ccyVar = ROOT.TH1F("ccyvar","ccyvar",100,0,1000)
		self.ncyVar = ROOT.TH1F("ncyvar","ncyvar",100,0,1000)
		self.ccyVarw = ROOT.TH1F("ccyvarw","ccyvarw",100,0,1000)
		self.ncyVarw = ROOT.TH1F("ncyvarw","ncyvarw",100,0,1000)
		self.ccDEVariation = ROOT.TH1F("ccdevar","ccdevar",1000,0,100)
		self.ncDEVariation = ROOT.TH1F("ncdevar","ncdevar",1000,0,100)
		self.ccMeanPE = ROOT.TH1F("ccmeanpe","ccmeanpe",1000,0,10000)
		self.ncMeanPE = ROOT.TH1F("ncmeanpe","ncmeanpe",1000,0,10000)
		self.ncDensity = ROOT.TH1F("ncdensity","ncdensity",100,0,1.0)
		self.ccDensity = ROOT.TH1F("ccdensity","ccdensity",100,0,1.0)
		self.ccMoliere = ROOT.TH2F("ccmol","ccmol",100,-50,50,1000,0.0,1.0)
		self.ncMoliere = ROOT.TH2F("ncmol","ncmol",100,-50,50,1000,0.0,1.0)

	def fill(self, ev):
		
		#for ev in events:
		totalPE = 0.0
		for digit in ev.digits:
			self.tempDigit.current = ev.current
			self.tempDigit.x = digit.x
			self.tempDigit.y = digit.y
			self.tempDigit.z = digit.z
			self.tempDigit.t = digit.t
			self.tempDigit.pe = digit.pe
			self.tempDigit.interactionType = digit.interactionType
			#print digit.pe
			totalPE += digit.pe
			self.tempDigit.event = digit.event
			self.tempDigit.plane = digit.plane
			if (digit.view == "X"):
				self.tempDigit.view = 0
			else:
				self.tempDigit.view = 1	
			self.tree.Fill()
		print totalPE
		self.tempEvent.coneAngle = ev.coneAngle
		self.tempEvent.coneDensity = ev.reconstructedVariables["coneDensity"]
		self.tempEvent.recE = ev.reconstructedVariables["neutrinoEnergy"]
		self.tempEvent.pid = ev.reconstructedVariables["pid"]
		self.tempEvent.interactionType = ev.interactionType
		self.tempEvent.vertexX = ev.vertexX
		self.tempEvent.vertexY = ev.vertexY	
		self.tempEvent.vertexZ = ev.vertexZ
		self.tempEvent.event = self.count
		self.tempEvent.totalPlanes = ev.stats["consecutivePlanes"]
		self.tempEvent.xVar = ev.stats["xVar"]
		if (ev.current == 1):	
			#for key in ev.reconstructedVariables["chargeCaptured"]:
			#	self.ccMoliere.Fill(key, ev.reconstructedVariables["chargeCaptured"][key])
			for x in range(0,int(ev.stats["xVar"]),10):
				self.ccxVar.Fill(x)	
			for y in range(0,int(ev.stats["yVar"]),10):
				self.ccyVar.Fill(y)	
			for xw in range(0,int(ev.stats["xVarw"]),10):
				self.ccxVarw.Fill(xw)	
			for yw in range(0,int(ev.stats["yVarw"]),10):
				self.ccyVarw.Fill(yw)
			for pe in range(0,int(totalPE),10):
				self.ccTotalPE.Fill(pe)	
			for mpe in range(0,int(ev.stats["meanPE"]),10):
				self.ccMeanPE.Fill(mpe)
			for pevar in [0.1*x for x in range(0,10*int(ev.stats["deVariation"]))]:
				self.ccDEVariation.Fill(pevar)
			for den in [0.01*x for x in range(0,int(100*ev.reconstructedVariables["coneDensity"]))]:
				self.ccDensity.Fill(den)
		
		if (ev.current == 0):
			#for key in ev.reconstructedVariables["chargeCaptured"]:
			#	self.ncMoliere.Fill(key, ev.reconstructedVariables["chargeCaptured"][key])
			for x in range(0,int(ev.stats["xVar"]),10):
				self.ncxVar.Fill(x)	
			for y in range(0,int(ev.stats["yVar"]),10):
				self.ncyVar.Fill(y)	
			for xw in range(0,int(ev.stats["xVarw"]),10):
				self.ncxVarw.Fill(xw)	
			for yw in range(0,int(ev.stats["yVarw"]),10):
				self.ncyVarw.Fill(yw)
			for pe in range(0,int(totalPE),10):
				self.ncTotalPE.Fill(pe)	
			for mpe in range(0,int(ev.stats["meanPE"]),10):
				self.ncMeanPE.Fill(mpe)	
			for pevar in [0.1*x for x in range(0,10*int(ev.stats["deVariation"]))]:
				self.ncDEVariation.Fill(pevar)	
			for den in [0.01*x for x in range(0,int(100*ev.reconstructedVariables["coneDensity"]))]:
				self.ncDensity.Fill(den)
		self.tempEvent.yVar = ev.stats["yVar"]
		self.tempEvent.totalPE = totalPE
		self.tempEvent.nuE = ev.nuEnergy
		self.tempEvent.current = ev.current
		print ev.current
		self.eventTree.Fill()

		for point in ev.spacePoints:
			self.tempSpacePoint.event = self.count#getattr(point,"event")
			self.tempSpacePoint.x = getattr(point,"x")
			self.tempSpacePoint.y = getattr(point,"y")
			self.tempSpacePoint.z = getattr(point,"z")
			self.pointTree.Fill()
		for planeKey in ev.planes:
			planeNo = ev.planes[planeKey]
			for view in ['X','Y']:
				plane = planeNo[view]
				hits =  plane.nFoundPeaks
				if hits > 100:
					hits = 100
				print "HITS ",
				print hits
				if hits > 0:
					for hit in range(hits):	
						if plane.view == "X":
							self.tempPlane.view = 0
						else:
							self.tempPlane.view = 1
						self.tempPlane.hitA = plane.showerPoints[hit]
						self.tempPlane.mean = plane.mean
						self.tempPlane.event = plane.event
						self.tempPlane.variance = plane.variance
						self.tempPlane.totalPE = plane.totalPE
						self.tempPlane.planeNumber = plane.planeNumber
						self.planeTree.Fill()
		for sheetKey in ev.sheets:
			sheet = ev.sheets[sheetKey]
			self.tempSheet.planeNumber = sheet.planeNumber
			self.tempSheet.event = sheet.event
			self.tempSheet.xMean = sheet.xMean
			self.tempSheet.yMean = sheet.yMean
			self.tempSheet.xExtrap = sheet.extrapolation["X"]
			self.tempSheet.yExtrap = sheet.extrapolation["Y"]
			self.sheetTree.Fill()
		self.count += 1
		#count += 1
		#self.rootFile.Write()

	def write(self):
		self.rootFile.Write()

	def makeGraphs(self, event, count):
		xMeans = array.array('f')
		xWidths = array.array('f')
		planes = array.array('f')
		totalPE = array.array('f')
		planeErrors = array.array('f')
		self.graphs = {}
		name = str(count) + "-" + str(event.current)	
		self.graphs["showerHistogram"] = ROOT.TH1F(name,name,2000,-1000,1000)
		for sheetKey in event.sheets:
			sheet = event.sheets[sheetKey]
			self.graphs["showerHistogram"].Fill(sheet.planeNumber, sheet.totalPE)
			planes.append(sheet.planeNumber)
			planeErrors.append(0.0)
			xMeans.append(sheet.xMean)
			xWidths.append(sheet.covariance[0][0])
		self.graphs["shower"] = ROOT.TGraphErrors(len(xMeans), planes, xMeans, planeErrors,xWidths)
		self.graphs["shower"].SetName(str(count))
		self.graphs["shower"].Write()
	#	self.graphs["showerHistogram"].Fit("gaus")
		self.graphs["showerHistogram"].Write()

	def prepareCharacterisation(self):
		self.ncDepthHist = ROOT.TH1F("nc_depth","nc_depth",100,0,100)
		self.ccDepthHist = ROOT.TH1F("cc_depth","cc_depth",100,0,100)
		self.deHist = ROOT.TH2F("de","de",100,0,100,1000,0,1000)
		self.ccdeHist = ROOT.TH2F("ccde","ccde",100,0,100,1000,0,1000)
		self.ncdeHist = ROOT.TH2F("ncde","ncde",100,0,100,1000,0,1000)
		sheetNo = 0	
		self.sheetNCHistograms = []
		self.sheetNCHistograms.append(ROOT.TH1F("de-" + str(sheetNo),str(sheetNo),1000,0,1000))		
		self.sheetCCHistograms = []
		self.sheetCCHistograms.append(ROOT.TH1F("de-" + str(sheetNo),str(sheetNo),1000,0,1000))
		
		self.sheetNCVarHistograms = []
		self.sheetNCVarHistograms.append(ROOT.TH1F("var-" + str(sheetNo),str(sheetNo),1000,0,1000))		
		self.sheetCCVarHistograms = []
		self.sheetCCVarHistograms.append(ROOT.TH1F("var-" + str(sheetNo),str(sheetNo),1000,0,1000))	


	def characteriseEvent(self, event):
		if (event.current == 0):
			sheetNo = 0
			for sheetKey in event.sheets:	
				#print sheetNo, len(sheetNCHistograms)
				if (sheetNo >= len(self.sheetNCHistograms)):
					print "Adding new hist"
					self.sheetNCHistograms.append(ROOT.TH1F("de-" + str(sheetNo),str(sheetNo),1000,0,1000))
					self.sheetNCVarHistograms.append(ROOT.TH1F("var-" + str(sheetNo),str(sheetNo),1000,0,1000))
				#print sheetNo, len(self.sheetNCHistograms)
				sheet = event.sheets[sheetKey]
				self.sheetNCHistograms[sheetNo].Fill(sheet.totalPE)
				self.sheetNCVarHistograms[sheetNo].Fill(sheet.covariance[0][0], sheet.totalPE)
				self.deHist.Fill(sheetNo,sheet.totalPE)
				self.ncdeHist.Fill(sheetNo,sheet.totalPE)
				self.ncDepthHist.Fill(sheetNo)
				sheetNo += 1

		if (event.current == 1):
			sheetNo = 0
			for sheetKey in event.sheets:	
				#print sheetNo, len(sheetCCHistograms)
				if (sheetNo >= len(self.sheetCCHistograms)):
					print "Adding new hist"
					self.sheetCCVarHistograms.append(ROOT.TH1F("var-" + str(sheetNo),str(sheetNo),1000,0,1000))
					self.sheetCCHistograms.append(ROOT.TH1F("de-"+str(sheetNo),str(sheetNo),1000,0,1000))
				#print sheetNo, len(sheetCCHistograms)
				sheet = event.sheets[sheetKey]
				self.sheetCCHistograms[sheetNo].Fill(sheet.totalPE)
				self.sheetCCVarHistograms[sheetNo].Fill(sheet.covariance[0][0], sheet.totalPE)
				self.deHist.Fill(sheetNo,sheet.totalPE)
				self.ccdeHist.Fill(sheetNo,sheet.totalPE)
				self.ccDepthHist.Fill(sheetNo)
				sheetNo += 1

	def finishCharacterisation(self):	
		h = 0
		cGraphs = []
		nclayers = array.array('f')
		ncmeanDEs = array.array('f')
		ncvarianceDEs = array.array('f')
		nclayerEs = array.array('f')
		
		ncvlayers = array.array('f')
		ncvVars = array.array('f')
		ncvVarsE = array.array('f')
		ncvlayerEs = array.array('f')
		for hist in self.sheetNCHistograms:
			nclayers.append(h)
			ncmeanDEs.append(hist.GetMean())
			try:
				ncvarianceDEs.append(hist.GetMean() / math.sqrt(hist.GetEntries()))
			except:
				ncvarianceDEs.append(0.0)
			nclayerEs.append(0.0)
			h += 1
			del hist
		h = 0
		for vhist in self.sheetNCVarHistograms:
			#Variances	
			ncvlayers.append(h)
			ncvVars.append(vhist.GetMean())
			try:
				ncvVarsE.append(vhist.GetMean() / math.sqrt(vhist.GetEntries()))	
			except:
				ncvVarsE.append(0.0)
			ncvlayerEs.append(0.0)
			h += 1
			del vhist
		meanDEGraph = ROOT.TGraphErrors(len(nclayers), nclayers, ncmeanDEs, nclayerEs, ncvarianceDEs)
		meanDEGraph.SetName("NCmeanDE")
		
		
		ncvarGraph = ROOT.TGraphErrors(len(ncvlayers), ncvlayers, ncvVars, ncvlayerEs, ncvVarsE)
		ncvarGraph.SetName("NCVar")
		
		

		ccvlayers = array.array('f')
		ccvVars = array.array('f')
		ccvVarsE = array.array('f')
		ccvlayerEs = array.array('f')
		cclayers = array.array('f')
		ccmeanDEs = array.array('f')
		ccvarianceDEs = array.array('f')
		cclayerEs = array.array('f')
		h = 0
		for hist in self.sheetCCHistograms:
			cclayers.append(h)
			ccmeanDEs.append(hist.GetMean())
			try:
				ccvarianceDEs.append(hist.GetMean() / math.sqrt(hist.GetEntries()))
			except:
				ccvarianceDEs.append(0.0)
			cclayerEs.append(0.0)
			h += 1
			del hist
		h = 0	
		for vhist in self.sheetCCVarHistograms:
			#Variances	
			ccvlayers.append(h)
			ccvVars.append(vhist.GetMean())
			try:
				ccvVarsE.append(vhist.GetMean() / math.sqrt(vhist.GetEntries()))
			except:
				ccvVarsE.append(0.0)
			ccvlayerEs.append(0.0)
			h += 1
			del vhist
			#print "CHECKING"
			#print vhist.GetMean()
		#self.rootFile = ROOT.TFile("events.root","recreate")
		ccmeanDEGraph = ROOT.TGraphErrors(len(cclayers), cclayers, ccmeanDEs, cclayerEs, ccvarianceDEs)
		ccmeanDEGraph.SetName("CCmeanDE")
		ccmeanDEGraph.Write()
		self.deHist.Write()
		self.ccdeHist.Write()
		self.ncdeHist.Write()
		
		ccvarGraph = ROOT.TGraphErrors(len(ccvlayers), ccvlayers, ccvVars, ccvlayerEs, ccvVarsE)
		ccvarGraph.SetName("CCVar")
		ccvarGraph.Write()
		self.ncDepthHist.Write()
		self.ccDepthHist.Write()
		meanDEGraph.Write()	
		ncvarGraph.Write()

	def characterise(self, events):
		ncDepthHist = ROOT.TH1F("nc_depth","nc_depth",100,0,100)
		ccDepthHist = ROOT.TH1F("cc_depth","cc_depth",100,0,100)
		deHist = ROOT.TH2F("de","de",100,0,100,1000,0,1000)
		sheetNo = 0	
		sheetNCHistograms = []
		sheetNCHistograms.append(ROOT.TH1F("de-" + str(sheetNo),str(sheetNo),1000,0,1000))		
		sheetCCHistograms = []
		sheetCCHistograms.append(ROOT.TH1F("de-" + str(sheetNo),str(sheetNo),1000,0,1000))
		
		sheetNCVarHistograms = []
		sheetNCVarHistograms.append(ROOT.TH1F("var-" + str(sheetNo),str(sheetNo),1000,0,1000))		
		sheetCCVarHistograms = []
		sheetCCVarHistograms.append(ROOT.TH1F("var-" + str(sheetNo),str(sheetNo),1000,0,1000))	

		h = 0
		cGraphs = []
		nclayers = array.array('f')
		ncmeanDEs = array.array('f')
		ncvarianceDEs = array.array('f')
		nclayerEs = array.array('f')
		
		ncvlayers = array.array('f')
		ncvVars = array.array('f')
		ncvVarsE = array.array('f')
		ncvlayerEs = array.array('f')

		print len(sheetNCHistograms)
		for event in events:
			if (event.current == 0):
				sheetNo = 0
				for sheetKey in event.sheets:	
					print sheetNo, len(sheetNCHistograms)
					if (sheetNo >= len(sheetNCHistograms)):
						print "Adding new hist"
						sheetNCHistograms.append(ROOT.TH1F("de-" + str(sheetNo),str(sheetNo),1000,0,1000))
						sheetNCVarHistograms.append(ROOT.TH1F("var-" + str(sheetNo),str(sheetNo),1000,0,1000))
					print sheetNo, len(sheetNCHistograms)
					sheet = event.sheets[sheetKey]
					sheetNCHistograms[sheetNo].Fill(sheet.totalPE)
					sheetNCVarHistograms[sheetNo].Fill(sheet.covariance[0][0], sheet.totalPE)
					deHist.Fill(sheetNo,sheet.totalPE)
					ncDepthHist.Fill(sheetNo)
					sheetNo += 1

			if (event.current == 1):
				sheetNo = 0
				for sheetKey in event.sheets:	
					print sheetNo, len(sheetCCHistograms)
					if (sheetNo >= len(sheetCCHistograms)):
						print "Adding new hist"
						sheetCCVarHistograms.append(ROOT.TH1F("var-" + str(sheetNo),str(sheetNo),1000,0,1000))
						sheetCCHistograms.append(ROOT.TH1F("de-"+str(sheetNo),str(sheetNo),1000,0,1000))
					print sheetNo, len(sheetCCHistograms)
					sheet = event.sheets[sheetKey]
					sheetCCHistograms[sheetNo].Fill(sheet.totalPE)
					sheetCCVarHistograms[sheetNo].Fill(sheet.covariance[0][0], sheet.totalPE)
					deHist.Fill(sheetNo,sheet.totalPE)
					ccDepthHist.Fill(sheetNo)
					sheetNo += 1
		for hist in sheetNCHistograms:
			nclayers.append(h)
			ncmeanDEs.append(hist.GetMean())
			ncvarianceDEs.append(hist.GetMean() / math.sqrt(hist.GetEntries()))
			nclayerEs.append(0.0)
			h += 1
		h = 0
		for vhist in sheetNCVarHistograms:
			#Variances	
			ncvlayers.append(h)
			ncvVars.append(vhist.GetMean())
			ncvVarsE.append(vhist.GetMean() / math.sqrt(vhist.GetEntries()))
			ncvlayerEs.append(0.0)
			h += 1
		meanDEGraph = ROOT.TGraphErrors(len(nclayers), nclayers, ncmeanDEs, nclayerEs, ncvarianceDEs)
		meanDEGraph.SetName("NCmeanDE")
		meanDEGraph.Write()
		
		ncvarGraph = ROOT.TGraphErrors(len(ncvlayers), ncvlayers, ncvVars, ncvlayerEs, ncvVarsE)
		ncvarGraph.SetName("NCVar")
		ncvarGraph.Write()
		

		ccvlayers = array.array('f')
		ccvVars = array.array('f')
		ccvVarsE = array.array('f')
		ccvlayerEs = array.array('f')
		cclayers = array.array('f')
		ccmeanDEs = array.array('f')
		ccvarianceDEs = array.array('f')
		cclayerEs = array.array('f')
		h = 0
		for hist in sheetCCHistograms:
			cclayers.append(h)
			ccmeanDEs.append(hist.GetMean())
			ccvarianceDEs.append(hist.GetMean() / math.sqrt(hist.GetEntries()))
			cclayerEs.append(0.0)
			h += 1
		h = 0	
		for vhist in sheetCCVarHistograms:
			#Variances	
			ccvlayers.append(h)
			ccvVars.append(vhist.GetMean())
			ccvVarsE.append(vhist.GetMean() / math.sqrt(vhist.GetEntries()))
			ccvlayerEs.append(0.0)
			h += 1
		ccmeanDEGraph = ROOT.TGraphErrors(len(cclayers), cclayers, ccmeanDEs, cclayerEs, ccvarianceDEs)
		ccmeanDEGraph.SetName("CCmeanDE")
		ccmeanDEGraph.Write()
		deHist.Write()
		
		ccvarGraph = ROOT.TGraphErrors(len(ccvlayers), ccvlayers, ccvVars, ccvlayerEs, ccvVarsE)
		ccvarGraph.SetName("CCVar")
		ccvarGraph.Write()
		ncDepthHist.Write()
		ccDepthHist.Write()
			


