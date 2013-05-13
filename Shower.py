import Sheet
import ConeFinder
import SpacePoint
import Digit

class Shower(object):
	def __init__(self):
		self.sheets = []
		self.cone = None

	def makeEnergyProfile(self):
		self.energyProfile = ROOT.TH1F()
		for sheet in self.sheet:
			self.energyProfile.Fill(sheet.planeNumber, sheet.totalPE)
			self.energyProfile.Fit("landau")
