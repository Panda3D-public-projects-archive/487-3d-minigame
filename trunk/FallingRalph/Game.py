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
from Objects import *
#import os
#from Utilities import *


#Note: If you have a favorite font you like (and you have the .ttf for it) you can use this line of code in the command line
# 	   to convert it to a .egg
#      egg-mkfont -o fontName.egg fontName.ttf

'''
###TODO LIST:
### Come up with a better name - Patrick
	
'''

def collGeom(obj, name, fromMask, intoMask, geomList):
	cNode = CollisionNode(name)
	cNode.setFromCollideMask(BitMask32(fromMask))
	cNode.setIntoCollideMask(BitMask32(intoMask))
	
	for g in geomList:
		cNode.addSolid(g)
	
	cNodePath = obj.attachNewNode(cNode)
	cNodePath.show()
	return cNodePath

######CONSTANTS######
#These are used in loading the avatars for the character selection screen.
LIST_OF_AVATARS = [ "models/ralph", "models/sonic","models/tails","models/eve"]
LIST_OF_SCALES = [ 1, .25,.25,1]
LIST_OF_POSITIONS = [Vec3(-15,-5,0), Vec3(-7,-5,0), Vec3(7,-5,0), Vec3(15,-5,0)]
LIST_OF_NAMES = ["Ralph","Sonic","Tails", "Eve"]
LIST_OF_TEXT_POS = [Vec3(-1.1,0,-0.5), Vec3(-0.55,0,-0.5), Vec3(0.55,0,-0.5), Vec3(1.1,0,-0.5)]

#Used in Avatar Movement
X_STRAFE = 0.5
Y_STRAFE = 0.5

#Points
LOOP_SCORE = 100
RING_SCORE = 0


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
		self.cameraPos = Vec3(0,0,50) #I'm using this to keep track of the camera's position since it won't get me its position
		base.camera.setPosHpr(self.cameraPos, Vec3(0, -90, 0))
		
		
		#Initialize Picker
		self.picker = Picker(fromMask=BitMask32(0x01), collideWithGeom=True)
		
		#Character Selection
		self.avatars = []
		self.names = []
		self.selectScreen()
		
		#Object Storage
		self.objects = []
		#Storage for rings
		self.rings = []
		
		#State Variables
		self.notSelected = True
		self.curAvatar = -1 #Used to determine which avatar to load
		
		
		#A dictionary of what keys are currently being pressed
		#The key events update this list, and our task will query it as input
		self.keys = {"moveLeft" : 0, "moveRight" : 0, "moveUp" : 0, "moveDown":0, "levelStart": 0}
		
		#Arrow Keys, used in movement
		self.accept("arrow_left", self.keys.update, [{"moveLeft":1}] )
		self.accept("arrow_left-up", self.keys.update, [{"moveLeft":0}] )
		self.accept("arrow_right", self.keys.update, [{"moveRight":1}] )
		self.accept("arrow_right-up", self.keys.update, [{"moveRight":0}] )
		self.accept("arrow_up", self.keys.update, [{"moveUp":1}] )
		self.accept("arrow_up-up", self.keys.update, [{"moveUp":0}] )
		self.accept("arrow_down", self.keys.update, [{"moveDown":1}] )
		self.accept("arrow_down-up", self.keys.update, [{"moveDown":0}] )
		self.accept("h", self.displayHelp)
		self.accept("space", self.keys.update, [{"levelStart":1}] )
		
		#Picking, Used in character selection.
		self.accept("mouse1", self.pick)
		
		#Quit game
		self.accept("escape", sys.exit)
		
		self.avatarSelectTask = taskMgr.add(self.avatarSelect, "avatarSelect")
		
		'''
		#If we want music just comment out this part and put the file below
		#Play music
		self.music = base.loader.loadSfx("music/special_stage.mp3")
		self.music.setLoop(True)
		self.music.play()
		'''
	'''
	### Name: selectScreen 
	### Author: Patrick Delaney
	### Parameters: None
	### Description: Loads the select screen.
	'''
	def selectScreen(self):
		text = "Select a Character! Click on any of the four below!"
		self.titleText = self.loadText("fonts/vector.egg","Title", text,TextNode.ACenter,VBase4(0,0,1,1),Vec3(0,0,0.90),0.1)
		
		
		#Load the avatars on the screen for initial selection
		#Load the text below the avatars as well
		for i in range(len(LIST_OF_AVATARS)):
			self.avatars.append(self.loadAvatar(LIST_OF_AVATARS[i],LIST_OF_SCALES[i],LIST_OF_POSITIONS[i]))
			self.names.append(self.loadText("fonts/vector.egg",LIST_OF_NAMES[i], LIST_OF_NAMES[i],
							  TextNode.ACenter,VBase4(0,0,1,1),LIST_OF_TEXT_POS[i],0.1) )
	'''
	### Name: avatarSelect
	### Author: Patrick Delaney
	### Parameters: task
	### Description: This method is a task that handles the character selection. Once the player has selected a character, it
	###				 removes itself from the task queue and adds the gameLoop task to the queue as well as loads the initial 
	###				 gamestate.
	'''
	def avatarSelect(self,task):
		if(self.curAvatar < 0): # If the player has not selected a character
			return task.cont
		else:
			self.cleanUpAvatars()
			self.player = Player(self.curAvatar)
			self.ignore("mouse1") #We don't need picking anymore
			#Now that the player has picked an avatar
			#Prepare initial game state and add gameLoop to the task list.
			self.gameTask = taskMgr.add(self.gameLoop, "gameloop")
			self.gameTask.last = 0
			#Load objects 
			self.loadObjects()
			#Setup Collisions
			self.setupCollisions()
			
			return task.done
	'''
	### Name: loadAvatar
	### Author: Patrick Delaney
	### Parameters: path - path to Model, Scale - scale for the model, pos - position of the model
	### Description: Loads an "avatar" for the player unto the screen. This is used in the character select screen.
	'''
	def loadAvatar(self,path,scale,pos):
		avatar = loader.loadModel(path)
		avatar.setCollideMask(0x01)
		avatar.reparentTo(render)
		avatar.setScale(scale)
		avatar.setPos(pos)
		avatar.setP(-90)
		return avatar
	#Only used in testing and also as a placeholder for when you finish the level loader, Tom.	
	def loadObjects(self):
		ring = Objects(RING,Vec3(0,0,-10))
		self.rings.append(ring.object)
		ring = Objects(RING,Vec3(10,0,-10))
		self.rings.append(ring.object)
		ring = Objects(RING,Vec3(5,0,-10))
		self.rings.append(ring.object)
		ring = Objects(RING,Vec3(-5,0,-10))
		self.rings.append(ring.object)
		ring = Objects(RING,Vec3(-10,0,-50))
		self.rings.append(ring.object)
		ring = Objects(RING,Vec3(-10,0,-200))
		self.rings.append(ring.object)
		
	'''
	### Name: loadText
	### Author: Patrick Delaney
	### Parameters: path - path to Font file,nodeName - name for text node, str - String to be displayed
	###				align- How to align the text, see Panda3D manual, color - color to set, MUST be of type VBase4
	###				pos - position of the text, scale - scale of the text, MUST be small because we are using 
	###				aspect2d, (Because aspect2d coords are between -1 and 1)
	### Description: Loads a text unto the screen. See parameters for what to input.
	'''
	def loadText(self,path,nodeName,str,align, color,pos,scale):
		font = loader.loadFont(path)
		text = TextNode(nodeName)
		text.setFont(font)
		text.setText(str)
		text.setAlign(align)
		textPath = aspect2d.attachNewNode(text)
		textPath.setColor(color)
		textPath.setPos(pos)
		textPath.setScale(scale)
		return textPath
	'''
	### Name: cleanUpAvatars 
	### Author: Patrick Delaney
	### Parameters: None
	### Description: Deletes everything from the character selection screen.
	'''
	def cleanUpAvatars(self):
		self.titleText.removeNode()
		for i in range(len(LIST_OF_AVATARS)):
			self.avatars[i].removeNode()
			self.names[i].removeNode()
	'''
	### Name: pick
	### Author: Dr.Zmuda - Modified by Patrick Delaney
	### Parameters: Nothing
	### Description: A modified picker method created by Dr.Zmuda, instead of deleting the select item, it sets the curAvatar
	###				 state variable to the avatars number. This makes that avatar, the players avatar for the game.
	'''
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
		#Will also need to update the camera's position
		self.updatePlayer(dt)
		#Updating the camera with the player is off until we have something in the background to compare it with.
		self.updateCamera()
		
		#Get the rings to rotate
		self.updateRings(dt)
		

		return task.cont #Makes game loop infinite
	def updatePlayer(self,dt):
		curPos = self.player.avatar.getPos()
		if(self.keys["moveLeft"]):
			curPos[0] -= X_STRAFE
		elif(self.keys["moveRight"]):
			curPos[0] += X_STRAFE
		elif(self.keys["moveUp"]):
			curPos[1] += Y_STRAFE
		elif(self.keys["moveDown"]):
			curPos[1] -= Y_STRAFE
		newPos = curPos  + self.player.getVelocity()*dt*10
		self.player.avatar.setPos(newPos)
	def updateCamera(self):
		#We will need to discuss boundaries
		#avatarPos = self.player.avatar.getPos()
		base.camera.setPos(self.player.avatar.getPos() + Vec3(0,0,50))
	def updateRings(self,dt):
		if(len(self.rings) is not 0):
			for ring in self.rings:
				rotate = HprInterval(ring,ring.getHpr() +Vec3(0,0,1),dt)
				rotate.start()
	def setupCollisions(self):
		# use an event collision handler (sends events on collisions)
		self.cHandler = CollisionHandlerEvent()
		# set the pattern for the event sent on collision
		# "enter" plus the name of the object collided into
		self.cHandler.addInPattern("collected-%in")
		
		# make a traverser and make it the default traverser
		self.cTrav = CollisionTraverser()
		base.cTrav = self.cTrav
		
		bounds = self.player.avatar.getBounds()
		center = bounds.getCenter()
		radius = bounds.getRadius()
		#TODO:Need to create a specfic collision solid for each avatar
		if(self.player.avatarChoice == SONIC):
			avatarNode = collGeom(self.player.avatar, 'Sonic', 0x01, 0x00, 
										[CollisionSphere(Point3(center + Point3(0,0,10)),radius*1.2),
										CollisionSphere(Point3(center + Point3(0,0,20)),radius*1.2)])
										
		self.cTrav.addCollider(avatarNode,self.cHandler)
		#Set up collisions for rings
		for ring in self.rings:
			collGeom(ring,"ring", 0x00,0x01,[CollisionSphere(Point3(0,0,0),1)])
		#collGeom(self.rings[0].object,"Ring0", 0x00,0x01,[CollisionSphere(Point3(0,0,0),1)])
		#Set up collisions for objects (We may need to organize all objects by their type. Since creating the collision spheres
		#May be a pain.
		
		self.accept("collected-ring",self.collectRing)
	
	def displayHelp(self):
		#Needs to Pause Game
		return;
	def collectRing(self,cEntry):
		print cEntry.getIntoNodePath().getName()
		print cEntry.getFromNodePath().getName()
		print "You collected a ring!"
		for ring in self.rings:
			print ring
		print cEntry.getIntoNodePath().getParent()
		self.rings.remove(cEntry.getIntoNodePath().getParent())
		cEntry.getIntoNodePath().getParent().remove()
		
	
	
world = World()  #Creates the world

run()   #Runs the game.