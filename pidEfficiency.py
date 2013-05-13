import sys
fname = sys.argv[1]

f = open(fname,'r')
lines = f.readlines()
nc = 0.0
cc = 0.0
ncGood = 0.0
ccGood = 0.0
for line in lines:
	line.strip("\n")
	lineA = line.split(' ')
	guess = int(lineA[0])
	true = int(lineA[1])


	#if (guess == true):	
#	print "Correct!"
	#else:
	#	print "WRONG!!"
	if (true == 0):
		nc += 1.0
		if (guess == 0 ):
			ncGood += 1.0
	if (true == 1):
		cc += 1.0
		if (guess == 1):
			ccGood += 1.0
	

print str('%.3f' % (100.0*(ncGood / nc))) + "% NC tagging efficiency"
print str('%.3f' % (100.0*(ccGood / cc))) + "% CC tagging efficiency"
