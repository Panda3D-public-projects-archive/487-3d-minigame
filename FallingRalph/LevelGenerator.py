from Objects import *;
from random import randint, choice, random;

import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import *
from math import sin, cos, pi
import math
import copy
from Player import *
from Picker import Picker
from LevelGenerator import *

class LevelGenerator: 
	NUMBEROFRINGS = 50;  	# density of the rings
	HEIGHT = -800;			# length of the course
	SECTIONHEIGHT = HEIGHT / NUMBEROFRINGS; # a constant that is used.
	
	def __init__(self, rings, diff, anvils):
		random.seed();
		totalsign = 0;
		totalsign2 = 0;
		self.rings = rings;
		self.diff = diff;
		self.anvils = anvils
		lastRing = [0,0];
		currentRing = [0,0];
		
		sign = [0,0]
		
		for i in range( self.NUMBEROFRINGS ):
			if(lastRing[0] <0):
				sign[0] = random.random() -.5; #make it more often plus when negative
			else:
				sign[0] = random.random()  - .7; #make it more often minus when positive
				
			if(lastRing[1] <0):
				sign[1] = random.random() - .5; #make it more often plus when negative
			else:
				sign[1] = random.random() - .7; #make it more often minus when positive
			
			currentRing =   [lastRing[0] + ( sign[0]  / math.fabs(sign[0])) * ( random.random() * (1 * self.diff/5) ) - ( .5 * self.diff/5 ) , 
			                 lastRing[1] + ( sign[1]  / math.fabs(sign[1])) * ( random.random() * (1 * self.diff/5) ) - ( .5 * self.diff/5 )];
			
			if(diff > 5 and random.random() < diff/100.0):
				anvil = Objects( ANVIL , Vec3(currentRing[0] + sign[0] * (40-diff)*(random.random() + .5), currentRing[1] + sign[0] * (40-diff)*(random.random() + .5), i * self.SECTIONHEIGHT));
				self.anvils.append(anvil.object)
			totalsign += ( sign[0]  / math.fabs(sign[0]));
			totalsign2 += ( sign[1]  / math.fabs(sign[1]));
			
			ring = Objects( TORUS , Vec3(currentRing[0], currentRing[1], i * self.SECTIONHEIGHT));
			self.rings.append(ring.object);
			lastRing[0] = currentRing[0];
			lastRing[1] = currentRing[1];
		print totalsign;
		print "\n"
		print totalsign2;