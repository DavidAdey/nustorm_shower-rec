import ROOT
import sys
import math
from Digit import *
import Event

types = {"qel":0, "dis":1, "res":2, "coh":3, "dfr":4, "imd":5, "nuel":6, "em":7}

def unpack(fName = sys.argv[1]):
	Events = []
	Digits = []
	e = Event.Event()
	lastEvent = 0
	fileName = fName#sys.argv[1]
	f = open(fileName,'r')
	nuE = 0.0
	states = []
	intType = ""
	current = -1
	while (1):
		lines = f.readlines(100000)
		if not lines:
			break
		for line in lines:
			lineA = line.split(' ')
			if (len(lineA) > 1):
				#print lineA
				if (lineA[1] == "TYPE"):
					intType = types[lineA[2].strip("\n")]
					states = []
				if (lineA[1] == "CURRENT"):
					if (lineA[2] == "nc"):
						current = 0
					elif (lineA[2] == "cc"):
						current = 1
						#print "cc"
					nuE = float(lineA[3])
				if (lineA[1] == "STATE"):
					states.append(int((lineA[2])))
				if (lineA[1] == "DIGITTHING"):
					eventno = int(lineA[2])
					if (eventno != lastEvent):
						ec = e
						#Events.append(ec)
						yield ec
						#print len(ec.digits)
						e = Event.Event()	
					x = float(lineA[3]) 
					y = float(lineA[4]) 
					pe = float(lineA[5])
					plane = float(lineA[6])
					view = (str(lineA[7])).rstrip()
					t = float(lineA[8])
					d = Digit(eventno, x, y, t, pe, plane, view, intType)
					#print d.event
					e.states = states
					e.interactionType = intType
					e.nuEnergy = nuE
					e.current = current
					e.digits.append(d)
					lastEvent = eventno
	#	count = 0	
	#for event in Events:
	#	print "ev " + str(count)
	#	print len(event.digits)
	#	count += 1
	#return Events

#e = unpack()
#print (e)
