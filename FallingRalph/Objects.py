'''###########################################################################################################################
### File: Objects.py
### Name: Patrick Delaney, Tom Williams, John Mannix
### Class: CSE 487
### Instructor: Dr.Zmuda
### Assignment: Assignment 3
### Files included: Utilities.py, brickout.py
### Description: This class makes all of the objects for our game. (An Object Factory)
################ 
'''
### Name: 
### Author: Patrick Delaney
### Parameters: 
### Description: 
'''
###########################################################################################################################'''
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import *
from math import sin, cos, pi,sqrt
from random import randint, choice, random
import cPickle, sys

#####CONSTANTS######

#Identifiers for objects
TORUS = 1 #Loop
RING  = 2 # Used as a different score modifer / Possible win condition. Just an idea. - Patrick
ANVIL = 3
#Ideas for TORUS
#Speed up loop - Makes you move faster
#Slow down loop - Makes you move slower
# These can stack/ undo each other
#Double Points loop - Doubles the amount of points you can get
#Damage loop - Takes points away
# All these loops could be designated by color

class Objects:
	
	#Once we determine what objects we want to use - I will modify the constructor here. It will be similar to the player 
	#Constructor. We should also implement a score. Maybe a special attribute as well. - Patrick
	'''
	### Name: __init__ (Overridden Constructor)
	### Author: Patrick Delaney
	### Parameters: type - integer identifer signifying what type of object. See Constants above.
	###				pos - position, num- Used in naming the object's collision node. E.g Ring1
	### Description: 
	'''
	def __init__(self,type,pos):
		self.type = type;
		if(type == TORUS):
			self.object = loader.loadModel("models/torus")
			self.object.setScale(2)
			self.object.setColor(255,215,0,1)   # Gold
		elif(type == RING):
			self.object = loader.loadModel("models/torus")
			self.object.setScale(0.5)
			self.object.setColor(255,215,0,1)   # Gold
			self.object.setTransparency(True)	
		elif( type == ANVIL):
			self.object = loader.loadModel("models/anvil");
			self.object.setTransparency( True);
			self.object.setScale(5);
		else:
			self.object = loader.loadModel("models/torus")
		self.object.setPos(pos)
		self.object.reparentTo(render)
			
	