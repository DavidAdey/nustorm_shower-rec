import ROOT
import sys
import math

fileName = sys.argv[1]
rootFile = ROOT.TFile(fileName, 'r')
tree = rootFile.Get("tree")
canvas = ROOT.TCanvas()
histName = "hist"

plots = {}
plots["nc"] = {}
plots["cc"] = {}
plots["nc"]["histograms"] = {}
plots["nc"]["names"] = {}
plots["cc"]["histograms"] = {}
plots["cc"]["names"] = {}

for currentType in ('nc', 'cc'):
	for event in range(tree.GetEntries()):
		histName = currentType + str(event)
		hist = ROOT.TH2F(histName, histName, 1000,-10000,10000,1000,-2500,2500)
		plots[currentType]["histograms"][event] = hist
		plots[currentType]["names"][event] = histName	

for currentType in (0, 1):
	for event in range(tree.GetEntries()):
		print currentType, event
		cutString = '(current == ' + str(currentType) + ')*(eventnumber == ' + str(event) + ')'
		#weightString = '(yview_adc + xview_adc)'
		#cutString += '*'
		#cutString += weightString
		print cutString
		exists = tree.Draw(('y:x>>' + plots[currentType]["names"][event]), cutString, 'colz')
		if (0):
			xprojection = plots[currentType]["histograms"][event].ProjectionX()
			yprojection = plots[currentType]["histograms"][event].ProjectionY()
			xbins = xprojection.GetNbinsX()
			ybins = yprojection.GetNbinsX()
			lowestXbin = 0 
			lowestYbin = 0
			highestXbin = xbins
			highestYbin = ybins
			for binNo in range(xbins):
				xBinValue = xprojection.GetBinContent(binNo)
				if (xBinValue):
					lowestXbin = binNo
					break
			for binNo in range(ybins):
				yBinValue = yprojection.GetBinContent(binNo)
				if (yBinValue):
					lowestYbin = binNo
					break
			for binNo in range(xbins):
				xBinValue = xprojection.GetBinContent(highestXbin)
				if (xBinValue):
					break
				else:
					highestXbin -= 1	
			for binNo in range(ybins):
				yBinValue = yprojection.GetBinContent(highestYbin)
				if (yBinValue):
					break
				else:
					highestYbin -= 1
			highestX = xprojection.GetBinContent(highestXbin)
			highestY = yprojection.GetBinContent(highestYbin)
			lowestX = xprojection.GetBinContent(lowestXbin)
			lowestY = yprojection.GetBinContent(lowestYbin)
			#plots[currentType]["histograms"][event].GetXaxis().SetLimits(lowestX, highestX)			
			#plots[currentType]["histograms"][event].GetYaxis().SetLimits(lowestY, highestY)
			plots[currentType]["histograms"][event].Draw("colz")
		if (exists):
			print "saving"
			canvas.SaveAs(currentType + str(event) + ".pdf")
			
