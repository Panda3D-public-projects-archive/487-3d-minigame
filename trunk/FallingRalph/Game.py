'''###########################################################################################################################
### File: Game.py
### Names: Patrick Delaney, Tom Williams, John Mannix
### Class: CSE 487
### Instructor: Dr.Zmuda
### Assignment: Assignment 4
### Files included: 
### Description: 
################ 
'''
### Name: 
### Author: 
### Parameters: 
### Description: 
'''
###########################################################################################################################'''
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import *
from math import sin, cos, pi
from random import randint, choice, random
#import cPickle, sys
from direct.task.Task import Task
import math
import copy
from Player import *
from Picker import Picker
#import os
#from Utilities import *

'''
###TODO LIST:
### Come up with a better name - Patrick
	
'''


#Constants
#These are used in loading the avatars for the character selection screen.
LIST_OF_AVATARS = [ "models/ralph", "models/sonic","models/tails","models/eve"]
LIST_OF_SCALES = [ 1, .25,.25,1]
LIST_OF_POSITIONS = [Vec3(-15,-5,0), Vec3(-7,-5,0), Vec3(7,-5,0), Vec3(15,-5,0)]


class World(DirectObject):
	'''
	### Name: __init__ (Constructor)
	### Author: Patrick Delaney
	### Parameters: 
	### Description: 
	'''
	def __init__(self):
		
		#Controls the size of the window
		wp = WindowProperties() 
		#wp.setFullscreen(1) 
		wp.setSize(1024, 768) 
		base.openMainWindow() 
		base.win.requestProperties(wp) 
		base.graphicsEngine.openWindows()
		
		# turn off default mouse motion and position camera
		# remember! if the mouse control is on, you can't reposition the camera
		base.disableMouse()
		base.camera.setPosHpr(Vec3(0,0,50), Vec3(0, -90, 0))
		
		
		#Initialize Picker
		self.picker = Picker(fromMask=BitMask32(0x01), collideWithGeom=True)
		
		#Character Selection
		self.avatars = []
		#Load the avatars on the screen for initial selection
		for i in range(len(LIST_OF_AVATARS)):
			self.avatars.append(self.loadAvatar(LIST_OF_AVATARS[i],LIST_OF_SCALES[i],LIST_OF_POSITIONS[i]))
		#self.avatarSelect()
		#base.camera.lookAt(self.player.avatar)
		
		#State Variables
		self.notSelected = True
		self.curAvatar = -1 #Used to determine which avatar to load
		
		'''
		#A dictionary of what keys are currently being pressed
		#The key events update this list, and our task will query it as input
		self.keys = {"moveLeft" : 0, "moveRight" : 0, "levelStart": 0}
		
		#Paddle Movement Commands
		#I may change this to an update paddle method similar to how AsteroidMouse updates the ship
		#self.accept("arrow_left", self.move, [1])
		#self.accept("arrow_right", self.move, [0])
		self.accept("arrow_left", self.keys.update, [{"moveLeft":1}] )
		self.accept("arrow_left-up", self.keys.update, [{"moveLeft":0}] )
		self.accept("arrow_right", self.keys.update, [{"moveRight":1}] )
		self.accept("arrow_right-up", self.keys.update, [{"moveRight":0}] )
		self.accept("h", self.displayHelp)
		self.accept("space", self.keys.update, [{"levelStart":1}] )
		'''
		self.accept("mouse1", self.pick)
		#Quit game
		self.accept("escape", sys.exit)
		
		self.avatarSelectTask = taskMgr.add(self.avatarSelect, "avatarSelect")
		'''
		#Register gameloop to the Task Manager
		self.gameTask = taskMgr.add(self.gameLoop, "gameloop")
		self.gameTask.last = 0
		'''
		
		'''
		#If we want music just comment out this part and put the file below
		#Play music
		self.music = base.loader.loadSfx("music/special_stage.mp3")
		self.music.setLoop(True)
		self.music.play()
		'''
		
		
	def avatarSelect(self,task):
		if(self.curAvatar < 0):
			return task.cont
		else:
			self.cleanUpAvatars()
			self.player = Player(self.curAvatar)
			self.ignore("mouse1") #We don't need picking anymore
			#Now that the player has picked an avatar
			#Prepare initial game state and add gameLoop to the task list.
			self.gameTask = taskMgr.add(self.gameLoop, "gameloop")
			self.gameTask.last = 0
			
			return task.done
		#while(charNotSelected){
			#self.player = Player(SONIC)
		#}
	def loadAvatar(self,path,scale,pos):
		avatar = loader.loadModel(path)
		avatar.setCollideMask(0x01)
		avatar.reparentTo(render)
		avatar.setScale(scale)
		avatar.setPos(pos)
		avatar.setP(-90)
		return avatar
	def cleanUpAvatars(self):
		for i in range(len(LIST_OF_AVATARS)):
			self.avatars[i].removeNode()
	def pick(self):
		cEntry = self.picker.pick()
		if cEntry:
			avatarGeomHit = cEntry.getIntoNodePath()
			for i in range(len(self.avatars)):
				p = self.avatars[i]
				if p.isAncestorOf(avatarGeomHit):
					self.curAvatar = i
					return
	def gameLoop(self, task):
		#Getting the change in time since the last task.
		dt = task.time - task.last
		task.last = task.time
		

		return task.cont #Makes game loop infinite
	def collisionDetection(self):
		return;
	
	def displayHelp(self):
		return;
		
	
	
world = World()  #Creates the world

run()   #Runs the game.