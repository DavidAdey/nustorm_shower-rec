import ROOTFileManager
import unpack
import SpacePointReconstructor
import SheetReconstructor
import PlaneReconstructor
import sys
sys.path.append("./LibraryEventMatching/")
import LEMCompactor
import ParameterCalculator
import BasicCutPID
import ConeFinder
import LikelihoodPID

codes = {"cc":1,"nc":0}
cctotal = 0.0
ccguess = 0.0
ccgood = 0.0
nctotal = 0.0
ncguess = 0.0
ncgood = 0.0
def pidEff(pid, totals):
	if (pid["true"] == 0):
		totals["nc"] += 1.0
		if (pid["guess"] == 0 ):
			totals["ncGood"] += 1.0
	elif (pid["true"] == 1):
		totals["cc"] += 1.0
		if (pid["guess"] == 1):
			totals["ccGood"] += 1.0
	
totals = {}
totals["nc"] = 0.0
totals["cc"] = 0.0
totals["ncGood"] = 0.0
totals["ccGood"] = 0.0
pidcutter = BasicCutPID.BasicCutPID()
pidcutter.setCuts(sys.argv[2],sys.argv[3],sys.argv[4])
pcalc = ParameterCalculator.ParameterCalculator()
events = unpack.unpack()
comp = LEMCompactor.LEMEventCompactor()
rm = ROOTFileManager.ROOTFileManager()
rm.setupTree()
#rm.prepareCharacterisation()
no = 0
allStats = []
lpid = LikelihoodPID.LikelihoodPID()
lpid.loadLikelihoods("ratios.root")
for event in events:
	no += 1
	print str(no) + " Events"
	if (1):#no < 100):

	#print "Event " + str(no)
	#print "Using " + str(len(event.digits))
	#print str(len(sprec.getPoints())) + " space points"
	#shrec = SheetReconstructor.SheetReconstructor()
	#shrec.sortPoints(event)
	#shrec.sortSheets()
	#print len(event.spacePoints)
	#event = shrec.filterPoints(event)
	#print len(event.spacePoints)
#for e in events:
#	print e
#	print len(e.spacePoints)"""
		
		#sprec = SpacePointReconstructor.SpacePointReconstructor()
		#sprec.makeSpacePoints(event, "makeAllPoints")
		pr = PlaneReconstructor.PlaneReconstructor()
		pr.sortDigits(event)
		pr.calculateVariables()
		event.planes = pr.getPlanes()
		shrec = SheetReconstructor.SheetReconstructor()
		shrec.makeFromPlanes(event)
		shrec.mergeAll()
		event.sheets = shrec.getSheets()
		#print len(event.sheets)
		cf = ConeFinder.ConeFinder()
		cf.process(event)
		#print "ANGLE"
		#print cf.angle
		event.coneAngle = cf.angle
		event.reconstructedVariables["coneDensity"] = cf.totalFraction
		#event.reconstructedVariables["coneAngle"] = cf.coneAngle
		event.reconstructedVariables["neutrinoEnergy"] = (event.totalPE/80.0) + ((event.totalPE/80.0)*((1.5*7.9*1.5)/(1.9*1.1*2.0)))
		event.reconstructedVariables["chargeCaptured"] = cf.chargeCaptured
		#rm.fill(event)
		#rm.makeGraphs(event, no)
		
		#comp.compact(event)	
		stats = pcalc.processEvent(event)
		event.stats = stats
		pid =  lpid.PID(event)
		#print pid
		#print event.current
		if (event.current == 0):
			nctotal += 1.0
			if (pid["pid"] == 0):
				ncgood += 1.0
				ncguess += 1.0
			if (pid["pid"] == 1):
				ccguess += 1.0

		if (event.current == 1):
			cctotal += 1.0
			if (pid["pid"] == 1):
				ccgood += 1.0
				ccguess += 1.0
			if (pid["pid"] == 0):
				ncguess += 1.0
		event.reconstructedVariables["pid"] = pid["pid"]
		
		rm.fill(event)
		#rm.characteriseEvent(event)
		#allStats.append(stats)
		#pidresult = pidcutter.PID(stats, event)
		#print pidresult["guess"], pidresult["true"]
		#pidEff(pidresult, totals)
"""
cceff = ccgood / cctotal
ccpure = ccgood / ccguess

nceff = ncgood / nctotal
ncpure = ncgood / ncguess
print "CC"
print str(100.0*cceff) + "% Efficient"
print str(100.0*ccpure) + "% Pure"

print "NC"
print str(100.0*nceff) + "% Efficient"
print str(100.0*ncpure) + "% Pure"
"""

#for stat in allStats:
	
#print str('%.3f' % (100.0*(totals["ncGood"] / totals["nc"]))) + "% NC tagging efficiency"
#print str('%.3f' % (100.0*(totals["ccGood"] / totals["cc"]))) + "% CC tagging efficiency"
#ccPure = totals["cc"] / (totals["cc"] + ((1.0 - totals["ncGood"])*totals["nc"]))
#print ccPure
#rm.finishCharacterisation()	
rm.write()

