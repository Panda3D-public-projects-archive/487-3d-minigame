'''###########################################################################################################################
### File: Player.py
### Name: Patrick Delaney, Tom WIlliams, John Mannix
### Class: CSE 487
### Instructor: Dr.Zmuda
### Assignment: Assignment 3
### Files included: Utilities.py, brickout.py
### Description: This class contains all of my methods that were global in nature in brickout.py
################ 
'''
### Name: 
### Author: Patrick Delaney
### Parameters: 
### Description: 
'''
###########################################################################################################################'''
import direct.directbase.DirectStart    # starts Panda
import sys

from pandac.PandaModules import *       # basic Panda modules
from direct.showbase.DirectObject import DirectObject   # for event handling
from direct.actor.Actor import Actor    # Actor class
from direct.interval.IntervalGlobal import *    # Intervals (Parallel, Sequence, etc)
from direct.task import Task    # for task contants
import math
import random


######CONSTANTS######
#CHOICE OF MODELS
RALPH = 0
SONIC = 1
TAILS = 2
EVE = 3
BUNNY = 4
STARTING_VELOCITY = Vec3(0,0,-10)
#################
SONIC_SCALE = .25
STARTING_POS = Vec3(0,0,0)


#####################

class Player:
	'''
	### Name: __init__ (Overriden Constructor) 
	### Author: Patrick Delaney
	### Parameters: choice - Choice of Model
	### Description: Constructs the Player Object
	'''
	def __init__(self,choice):
		#self.avatarNode = render.attachNewNode("player_dummy_node")
		if(choice == RALPH):
			self.avatar = loader.loadModel("models/ralph")
		elif(choice == SONIC):
			self.avatar = loader.loadModel("models/sonic")
			self.avatar.setScale(SONIC_SCALE)
		elif(choice == TAILS):
			self.avatar = loader.loadModel("models/tails")
			self.avatar.setScale(SONIC_SCALE)
		elif(choice == EVE):
			self.avatar = loader.loadModel("models/eve")
		elif(choice == BUNNY):
			self.avatar = loader.loadModel("models/bunny")
		self.avatar.reparentTo(render)
		self.avatar.setPos(STARTING_POS)
		self.avatar.setHpr(180,90,0)
		self.avatar.setTransparency(False)
		self.velocity = STARTING_VELOCITY
		self.avatarChoice = choice
	def getVelocity(self):
		return self.velocity
	def setVelocity(self,val):
		self.velocity = val
	
		