import math
import SpacePoint
import Globals

def chi2(pointA, pointB):
	xResidual = math.pow(getattr(pointA, "x") - getattr(pointB, "y"),2)
	yResidual = math.pow(getattr(pointA, "y") - getattr(pointB, "y"),2)
	residual = math.sqrt(xResidual + yResidual)
	return residual

def findDigitNo(value):
	digitNo = int(value/Globals.CHANNELWIDTH)
	return digitNo

def findCompactionDivision(value, center):
	digitGroup = 0
	difference = value - center
	for group in range(100,1,-1):
		#print group
		groupSum = sumLower(group-1, center)
		#print groupSum, int(math.fabs(difference))
		if (math.fabs(difference) == 1):
			digitGroup = (1)*(difference/math.fabs(difference))
			break
		elif (int(math.fabs(difference) > sumLower(group-1, center))):
			#print "Yes"
			#print difference, groupSum, group
			if (difference == 0):
				pass
			else:
				digitGroup = (group)*(difference/math.fabs(difference))
			break
	return digitGroup
	
def sumLower(value, mean):
	total = 0
	for i in range(value, 0, -1):
		#print value, i
		total += i
	return total

#for i in range(-60,60):
#	print i, findCompactionDivision(i, 30)
