'''###########################################################################################################################
### File: Game.py
### Names: Patrick Delaney, Tom Williams, John Mannix
### Class: CSE 487
### Instructor: Dr.Zmuda
### Assignment: Assignment 4
### Files included: 
### Description: 
### Note: Sonic the Hedgehog and other names are registered trademarks of SEGA. This game is only made for academic purposes.
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
from LevelGenerator import *
#import os
#from Utilities import *


#Note: If you have a favorite font you like (and you have the .ttf for it) you can use this line of code in the command line
# 	   to convert it to a .egg
#      egg-mkfont -o fontName.egg fontName.ttf

'''
###TODO LIST/ IDEAS:
### Come up with a better name
### Create a Splash Screen
### Create the Level Select Screen
### Create the Help Screen
### Create Custom Level Loaders and 10-20 Levels
### Add more objects
### Implement an end to a level
### Add a results screen  (Return back to level select screen afterwards?)	
### Add a button that causes the players avatar to speed up / slow down
'''
'''
### Name: collGeom
### Author: Dr. Zmuda 
### Parameters: obj- object, name - name of the object, fromMask - Bit Mask for from collide check, intoMask - Bit mask for 
###				into collide check, geomList - list of collision geometic objects
### Description: Factored out code that simplifies creating collision objects.
'''
def collGeom(obj, name, fromMask, intoMask, geomList):
	cNode = CollisionNode(name)
	cNode.setFromCollideMask(BitMask32(fromMask))
	cNode.setIntoCollideMask(BitMask32(intoMask))
	
	for g in geomList:
		cNode.addSolid(g)
	
	cNodePath = obj.attachNewNode(cNode)
	#cNodePath.show()
	return cNodePath
	
######CONSTANTS######
#These are used in loading the avatars for the character selection screen.
LIST_OF_AVATARS = [ "models/ralph", "models/sonic","models/tails","models/eve"]
LIST_OF_SCALES = [ 1, .25,.25,1]
LIST_OF_POSITIONS = [Vec3(-15,-5,0), Vec3(-7,-5,0), Vec3(7,-5,0), Vec3(15,-5,0)]
LIST_OF_NAMES = ["Ralph","Sonic","Tails", "Eve"]
LIST_OF_TEXT_POS = [Vec3(-1.1,0,-0.5), Vec3(-0.55,0,-0.5), Vec3(0.55,0,-0.5), Vec3(1.1,0,-0.5)]

#Used in Avatar Movement
X_STRAFE = .5
Y_STRAFE = .5

#Points
LOOP_SCORE = 100
RING_SCORE = 0
ANVIL_LOSS = 5

#Used in the level select scene
LIST_OF_DIFFICULT = ["easy","normal","hard","intense","insane","bunnies"]
DSCALE = Vec3(4,1,16)
LIST_OF_DPOS = [Vec3(-10,0,0),Vec3(-6,0,0),Vec3(-2,0,0),Vec3(2,0,0),Vec3(6,0,0),Vec3(10,0,0)]

#Difficulty levels
SCALE_OF_HARDNESS = [5,10,15,20,25,25]
BUNNIES = 25


class World(DirectObject):
	'''
	### Name: __init__ (Constructor)
	### Author: Patrick Delaney, Tom Williams, John Mannix
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
		#Level selection
		self.buttons = []
		self.curDiff = -1
		
		#Object Storage
		self.objects = []
		#Storage for rings
		self.rings = []
		self.types = []
		#Storage for anvils
		self.anvils = []
		#Storage for collisionNodes
		self.cNodePaths = []
		self.helpScreenOn = 0
		self.inGame = False
		
		#State Variables
		self.notSelected = True
		self.curAvatar = -1 #Used to determine which avatar to load
		self.score = 0 #Used to keep track of the player's score.
		self.numRings = 0 #Used to keep track of how many Rings Collected
		self.alreadyDisplayed = False
		self.endOfLevel = False #Used to keep track of when the player hits the end of the level.
		self.resetGame = False #Used to decide when to reset the game
		
		
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
		
		self.accept("mouse1", self.introClick)
		
		#Quit game
		self.accept("escape", sys.exit)
		
		self.introWaitTask = taskMgr.add(self.introWait, "introWait")
		
		#Music for the game
		self.ringLoss = base.loader.loadSfx("music/RingLoss.mp3")
		self.ringGained = base.loader.loadSfx("music/RingGained.mp3")
		self.stageSelectMusic = base.loader.loadSfx("music/LevelSelect.mp3")
		self.helpMusic = base.loader.loadSfx("music/HelpMusic.mp3")
		self.characterSelectMusic = base.loader.loadSfx("music/SelectACharacter.mp3")
		#self.gameMusic = base.loader.loadSfx("music/special_stage.mp3")
		self.gameMusic = base.loader.loadSfx("music/special_stage_2.mp3")
		self.introMusic = base.loader.loadSfx("music/IntroMusic.mp3")
		self.badEndingMusic = base.loader.loadSfx("music/StageClearBad.mp3")
		self.goodEndingMusic = base.loader.loadSfx("music/StageClear.mp3")
		
		self.introScreen()
		

	'''
	### Name: introScreen
	### Author: John Mannix
	### Parameters: Nothing
	### Description: Sets up the intro screen 
	'''	
	def introScreen(self):
		self.introMusic.play()
		self.readyClick = 0
		self.titleScreen = loader.loadModel("models/plane")
		tex = loader.loadTexture("models/titleScreen.png")
		self.titleScreen.setTexture(tex, 1)  
		self.titleScreen.setCollideMask(0x01)
		self.titleScreen.reparentTo(render)
		self.titleScreen.setScale(Vec3(16,1,16))
		self.titleScreen.setPos(Vec3(0,0,0))
		self.titleScreen.setP(-90)
	'''
	### Name: introClick
	### Author: John Mannix
	### Parameters: nothing
	### Description: sets up state for the next screen after the intro screen
	'''	
	def introClick(self):
		self.ignore("mouse1")
		self.readyClick = 1
	'''
	### Name: introWait
	### Author: John Mannix
	### Parameters: task - required for task methods
	### Description: The task that handles the introscreen.
	'''	
	def introWait(self, task):
		if self.readyClick == 0:
			return task.cont
		else:
			self.titleScreen.removeNode()
			if self.introMusic.status() == self.introMusic.PLAYING:
				self.introMusic.stop()
			self.selectLevel()
			self.accept("mouse1", self.buttonPick) #Picking, Used in character selection and level selection.
			self.buttonSelectTask = taskMgr.add(self.buttonSelect, "buttonSelect")
			return task.done
	'''
	### Name: loadButton
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: path - path to texture, scale - scale of button, pos- position of button
	### Description: Loads the buttons for the difficulty select screen
	'''	
	def loadButton(self,path,scale,pos):
		button = loader.loadModel("models/plane")
		tex = loader.loadTexture("models/button-"+path+".png") #Load the texture
		button.setTexture(tex, 1)  
		button.setCollideMask(0x01)
		button.reparentTo(render)
		button.setScale(scale)
		button.setPos(pos)
		button.setP(-90)
		return button
	'''
	### Name: selectLevel
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: None
	### Description: Sets up the difficulty select screen
	'''	
	def selectLevel(self):
		self.stageSelectMusic.setLoop(True)
		self.stageSelectMusic.play()
		text = "Select your Level!"
		self.titleText = self.loadText("fonts/centbold.egg","Title", text,TextNode.ACenter,VBase4(0,0,1,1),Vec3(0,0,0.90),0.1)
		
		for i in range(len(LIST_OF_DIFFICULT)):
			self.buttons.append(self.loadButton(LIST_OF_DIFFICULT[i], DSCALE, LIST_OF_DPOS[i]))

	'''
	### Name: buttonSelect
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: task - required for task methods
	### Description: The task that handles the difficulty select screen
	'''	          
	def buttonSelect(self,task):
		if(self.curDiff < 0): # If the player has not selected a level
			return task.cont
		else:
			self.cleanUpButtons()
			self.stageSelectMusic.stop()
			self.accept("mouse1", self.pick) # change picker to handle Avatars now.
			self.difficulty = SCALE_OF_HARDNESS[self.curDiff]
			self.selectScreen()
			self.avatarSelectTask = taskMgr.add(self.avatarSelect, "avatarSelect")
			#Start Character Select Music
			self.characterSelectMusic.setLoop(True)
			self.characterSelectMusic.play()
			return task.done
	'''
	### Name: buttonPick
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: nothing
	### Description: Handles picking for the buttons
	'''	
	def buttonPick(self):
		cEntry = self.picker.pick()
		if cEntry:
			buttonGeomHit = cEntry.getIntoNodePath()
			for i in range(len(self.buttons)):
				p = self.buttons[i]
				if p.isAncestorOf(buttonGeomHit):
					self.curDiff = i
					return
	'''
	### Name: cleanUpButtons
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: nothing
	### Description: Removes all the buttons from the screen
	'''	
	def cleanUpButtons(self):
		self.titleText.removeNode()
		for i in range(len(LIST_OF_DIFFICULT)):
			self.buttons[i].removeNode()
	'''
	### Name: selectScreen 
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: None
	### Description: Loads the select screen.
	'''
	def selectScreen(self):
		text = "Select a Character! Click on any of the four below!"
		self.titleText = self.loadText("fonts/centbold.egg","Title", text,TextNode.ACenter,VBase4(0,0,1,1),Vec3(0,0,0.90),0.1)
		
		
		#Load the avatars on the screen for initial selection
		#Load the text below the avatars as well
		if(self.curDiff <> 5):
			for i in range(len(LIST_OF_AVATARS)):
				self.avatars.append(self.loadAvatar(LIST_OF_AVATARS[i],LIST_OF_SCALES[i],LIST_OF_POSITIONS[i]))
				self.names.append(self.loadText("fonts/centbold.egg",LIST_OF_NAMES[i], LIST_OF_NAMES[i],
								  TextNode.ACenter,VBase4(0,0,1,1),LIST_OF_TEXT_POS[i],0.1) )
		else:
			self.avatars.append(self.loadAvatar("models/bunny",1,Vec3(0,0,0)))
			self.names.append(self.loadText("fonts/centbold.egg","Bunny", "Bunny",
								  TextNode.ACenter,VBase4(0,0,1,1),Vec3(0,-10,0),0.1) )
			self.curAvatar = BUNNY
	'''
	### Name: avatarSelect
	### Author: Patrick Delaney, Tom Williams, John Mannix
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
			self.loadInitialGameState()
			self.characterSelectMusic.stop()
			self.gameMusic.setLoop(True)
			self.gameMusic.play()
			
			return task.done
	'''
	### Name: loadAvatar
	### Author: Patrick Delaney, Tom Williams, John Mannix
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
	'''
	### Name: loadObjects
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: none
	### Description: Loads the objects in from the random level generator
	'''	
	def loadObjects(self):
		level = LevelGenerator( self.rings , self.difficulty, self.anvils);
	'''
	### Name: loadInitialGameState
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: none
	### Description: Prepares the initial game state and starts the main game loop.
	'''	
	def loadInitialGameState(self):
		self.gameTask = taskMgr.add(self.gameLoop, "gameloop")
		self.gameTask.last = 0
		#Load environment
		self.env = loader.loadModel("models/env")
		self.env.reparentTo(render)
		self.env.setScale(1000)
		self.env.setH(0)
		self.env.setPos(0,0,-1000)
		#Load objects 
		self.loadObjects()
		#Setup Collisions
		self.setupCollisions()
		
		self.inGame = True
		#Load score Font
		self.scoreText = self.loadText("fonts/centbold.egg","Score", "Score: " + `self.score`,TextNode.ACenter,
										VBase4(1,1,0,1),Vec3(-1.1,0,0.90),0.1)
		#Load Rings Font
		self.ringText = self.loadText("fonts/centbold.egg","Rings", "Rings: " + `self.numRings`,TextNode.ACenter,
										VBase4(1,1,0,1),Vec3(-1.1,0,0.70),0.1)
		#Allow Spacebar to be pressed to start the level
		self.accept("space", self.keys.update, [{"levelStart":1}] )
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
		for i in range(len(self.avatars)):
			self.avatars[i].removeNode()
			self.names[i].removeNode()
	'''
	### Name: pick
	### Author: Dr.Zmuda - Modified by Patrick Delaney
	### Parameters: Nothing
	### Description: A modified picker method created by Dr.Zmuda, instead of deleting the selected item, it sets the curAvatar
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
	'''
	### Name: gameLoop
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: 
	### Description: 
	'''	
	def gameLoop(self, task):
		#Getting the change in time since the last task.
		dt = task.time - task.last
		task.last = task.time
		if self.helpScreenOn == 1: #doesn't update while game is paused
			return task.cont
		
		if(self.keys["levelStart"]):
			if( not self.endOfLevel):
				#Remove the Instruction Text from the screen
				self.startText.removeNode()
				#Will also need to update the camera's position
				self.updatePlayer(dt)
				#Updating the camera.
				self.updateCamera()
		
				#Get the rings to rotate
				self.updateRings(dt)
			else:
				self.resultScreen()
				return task.done
		else:
			if(not self.alreadyDisplayed):
				self.startText = self.loadText("fonts/centbold.egg","Start", "Press 'Spacebar' to start",TextNode.ACenter,
										VBase4(0,0,0,1),Vec3(0,0,0),0.1)
				self.alreadyDisplayed = True

		return task.cont #Makes game loop infinite
	'''
	### Name: updatePlayer
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: dt - change in time 
	### Description: Updates the player using simple position equation. Physically stops the player from moving since the
	### 			 collision with the ground was not working right.
	'''	
	def updatePlayer(self,dt):
		
		curPos = self.player.avatar.getPos()
		if (curPos[2] <= -995):
			self.endOfLevel = True
			return
		if(self.keys["moveLeft"]):
			curPos[0] -= X_STRAFE
		if(self.keys["moveRight"]):
			curPos[0] += X_STRAFE
		if(self.keys["moveUp"]):
			curPos[1] += Y_STRAFE
		if(self.keys["moveDown"]):
			curPos[1] -= Y_STRAFE
		newPos = curPos  + self.player.getVelocity()*dt*10
		self.player.avatar.setPos(newPos)
	
	def updateCamera(self):

		base.camera.setPos(self.player.avatar.getPos() + Vec3(0,0,50))
	'''
	### Name: updateRings
	### Author: Patrick Delaney
	### Parameters:  dt - change in time since the last frame
	### Description: Causes the rings to rotate.
	'''
	
	def updateRings(self,dt):
		if(len(self.rings) is not 0):
			for ring in self.rings:
				rotate = HprInterval(ring,ring.getHpr() +Vec3(0,0,1),dt)
				rotate.start()
	'''
	### Name: setupCollisions
	### Author: Patrick Delaney
	### Parameters: None
	### Description: Sets up all of the collision objects.
	'''	
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
		#Creating Specific Collision Solids for each character
		if(self.player.avatarChoice == RALPH):
			avatarNode = collGeom(self.player.avatar, 'ralph', 0x01, 0x00, 
										[CollisionSphere(Point3(center + Point3(0.3,0,4.5)),radius*0.3),
										CollisionSphere(Point3(center + Point3(0.3,0,2.5)),radius*0.3),
										CollisionSphere(Point3(center + Point3(0.3,0,1.0)),radius*0.3)])
		elif(self.player.avatarChoice == SONIC):
			avatarNode = collGeom(self.player.avatar, 'sonic', 0x01, 0x00, 
										[CollisionSphere(Point3(center + Point3(0.2,0,25)),radius*1.1),
										CollisionSphere(Point3(center + Point3(0,0,15)),radius*1.1),
										CollisionSphere(Point3(center + Point3(-1,0,7)),radius)])
		elif(self.player.avatarChoice == TAILS):
			avatarNode = collGeom(self.player.avatar, 'tails', 0x01, 0x00, 
										[CollisionSphere(Point3(center + Point3(0,0,20)),radius*1.2),
										CollisionSphere(Point3(center + Point3(0,0,10)),radius*1.2),
										CollisionSphere(Point3(center + Point3(0,0,2)),radius)])
		
		elif(self.player.avatarChoice == EVE):
			avatarNode = collGeom(self.player.avatar, 'eve', 0x01, 0x00, 
										[CollisionSphere(Point3(center + Point3(0,0,3.5)),radius*0.35),
										CollisionSphere(Point3(center + Point3(0,0,1.75)),radius*0.35),
										CollisionSphere(Point3(center + Point3(0,0,0.35)),radius*0.3)])
		elif(self.player.avatarChoice == BUNNY):
			avatarNode = collGeom(self.player.avatar, 'bunny', 0x01, 0x00, 
										[CollisionSphere(Point3(center + Point3(0,0,3.5)),radius*0.35),
										CollisionSphere(Point3(center + Point3(0,0,1.75)),radius*0.35),
										CollisionSphere(Point3(center + Point3(0,0,0.35)),radius*0.3)])
										
										
		self.cTrav.addCollider(avatarNode,self.cHandler)
		self.cNodePaths.append(avatarNode)
		#Set up collisions for rings
		for ring in self.rings:
				self.cNodePaths.append(collGeom(ring,"ring", 0x00,0x01,[CollisionSphere(Point3(0,0,0),1)]) )
			
		for anvil in self.anvils:
				self.cNodePaths.append(collGeom(anvil,"anvil", 0x00,0x01,[CollisionSphere(Point3(0,0,0),0.5)]) )
		
		self.accept("collected-ring",self.collectRing)
		self.accept("collected-anvil",self.collectAnvil)

	def helpScreenToggle(self, tog):
		if tog == 1:
			self.help1 = self.loadText("fonts/centbold.egg","RingResult", "Controls",TextNode.ACenter,VBase4(1,1,0,1),Vec3(0,0,0.7),0.1)
			self.help2 = self.loadText("fonts/centbold.egg","RingResult", "Movement: Arrow Keys",TextNode.ACenter,VBase4(1,1,0,1),Vec3(0,0,0.5),0.1)
			self.help3 = self.loadText("fonts/centbold.egg","RingResult", "Help: H",TextNode.ACenter,VBase4(1,1,0,1),Vec3(0,0,0.3),0.1)
			self.help4 = self.loadText("fonts/centbold.egg","RingResult", "Exit Game: Escape",TextNode.ACenter,VBase4(1,1,0,1),Vec3(0,0,0.1),0.1)
			self.help5 = self.loadText("fonts/centbold.egg","RingResult", "Collect as many rings as you can",
																TextNode.ACenter,VBase4(1,1,0,1),Vec3(0,0,-0.1),0.1)
			self.help6 =  self.loadText("fonts/centbold.egg","RingResult", "to increase your score!",
																TextNode.ACenter,VBase4(1,1,0,1),Vec3(0,0,-0.2 ),0.1)
			self.help7 = self.loadText("fonts/centbold.egg","RingResult", "Watch out for Obstacles!",
																	TextNode.ACenter,VBase4(1,1,0,1),Vec3(0,0,-0.5),0.1)
		else:
			self.help1.removeNode()
			self.help2.removeNode()
			self.help3.removeNode()
			self.help4.removeNode()
			self.help5.removeNode()
			self.help6.removeNode()
			self.help7.removeNode()
	
	def displayHelp(self):
		if(self.inGame):  # Note only displays while in the game. Will not display otherwise. (Causes game to crash)
			if self.helpScreenOn == 0:
				self.helpScreenOn = 1
				self.env.hide()
				self.player.avatar.hide()
				for ring in self.rings:
					ring.hide()
				for anvil in self.anvils:
					anvil.hide()
				self.gameMusic.stop()
				self.helpMusic.setLoop(True)
				self.helpMusic.play()
				self.helpScreenToggle(1)
			else:
				self.helpScreenOn = 0
				self.helpScreenToggle(0)
				self.env.show()
				self.player.avatar.show()
				for ring in self.rings:
					ring.show()
				for anvil in self.anvils:
					anvil.show()
				self.helpMusic.stop()
				self.gameMusic.play()
		return
		
	'''
	### Name: collectAnvil
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: cEntry - required for collision events
	### Description: Causes the player to lose 5 rings if they hit an anvil
	'''		
	def collectAnvil(self,cEntry):
		print "You hit an anvil!"
		self.anvils.remove(cEntry.getIntoNodePath().getParent())
		cEntry.getIntoNodePath().getParent().remove()
		if(self.numRings < ANVIL_LOSS):
			self.numRings = 0
		else:
			self.numRings -= ANVIL_LOSS
		self.ringLoss.play()
		self.ringText.removeNode()
		self.ringText = self.loadText("fonts/centbold.egg","Rings", "Rings: " + `self.numRings`,
										TextNode.ACenter,VBase4(1,1,0,1),Vec3(-1.1,0,0.70),0.1)
	'''
	### Name: collectRing
	### Author: Patrick Delaney, Tom Williams, John Mannix
	### Parameters: cEntry - required for collision events
	### Description: Causes the player to gain a ring if the hit an onscreen ring
	'''		
	def collectRing(self,cEntry):
		print "You collected a ring!"
		self.rings.remove(cEntry.getIntoNodePath().getParent())
		cEntry.getIntoNodePath().getParent().remove()
		self.numRings += 1
		self.ringGained.play()
		#Update the Ring Text
		self.ringText.removeNode()
		self.ringText = self.loadText("fonts/centbold.egg","Rings", "Rings: " + `self.numRings`,
										TextNode.ACenter,VBase4(1,1,0,1),Vec3(-1.1,0,0.70),0.1)
		
	def resultScreen(self):
		self.env.hide()
		self.player.avatar.hide()
		self.gameMusic.stop()
		if self.numRings < 5:
			self.badEndingMusic.play()
		else:
			self.goodEndingMusic.play()
		self.ringText.removeNode()
		self.scoreText.removeNode()
		self.resultText = self.loadText("fonts/centbold.egg","Result", "RESULTS",
										TextNode.ACenter,VBase4(1,1,0,1),Vec3(0,0,0.9),0.1)
		collectedRings = 0
		self.ringResult = self.loadText("fonts/centbold.egg","RingResult", "You've Collected: " + `self.numRings` 
										+ " rings",TextNode.ACenter,VBase4(1,1,0,1),Vec3(-0.6,0,0.7),0.1)
		self.score += self.numRings*10
		self.scoreResultText = self.loadText("fonts/centbold.egg","scoreRes","Your score is now: " + `self.score` 
										     ,TextNode.ACenter,VBase4(1,1,0,1),Vec3(-0.6,0,0.5),0.1)
		self.continueText = self.loadText("fonts/centbold.egg","reset","Press r to go back to the Main Menu"
										     ,TextNode.ACenter,VBase4(1,1,0,1),Vec3(0.0,0,0.3),0.1)
		self.accept("r", self.reset)
		self.inGame = False
		self.waitTask = taskMgr.add(self.wait, "wait")
	def wait(self,task):
		if(not self.resetGame):
			return task.cont
		else:
			self.ignore("r")
			if self.badEndingMusic.status() == self.badEndingMusic.PLAYING:
				self.badEndingMusic.stop()
			if self.goodEndingMusic.status() ==	 self.goodEndingMusic.PLAYING:
				self.goodEndingMusic.stop()
			self.selectLevel()
			self.resetGame = False
			self.buttonSelectTask = taskMgr.add(self.buttonSelect, "buttonSelect")
			return task.done
	def reset(self):
		#Reset state variables
		self.notSelected = True
		self.resetGame = True
		self.endOfLevel = False
		self.alreadyDisplayed = False
		self.curAvatar = -1
		self.keys["levelStart"] = 0
		self.curDiff = -1
		self.numRings = 0
		self.inGame = False
		#Remove Objects
		self.env.removeNode()
		self.player.avatar.removeNode()
		for path in self.cNodePaths:
			path.removeNode()
		for ring in self.rings:
			ring.removeNode()
		for anvil in self.anvils:
			anvil.removeNode()
		#Remove text
		self.resultText.removeNode()
		self.ringResult.removeNode()
		self.scoreResultText.removeNode()
		self.continueText.removeNode()
		#Empty object storage
		del self.rings[:]
		del self.anvils[:]
		del self.buttons[:]
		del self.avatars[:]
		del self.names[:]
		#Reset camera
		self.cameraPos = Vec3(0,0,50) #I'm using this to keep track of the camera's position since it won't get me its position
		base.camera.setPosHpr(self.cameraPos, Vec3(0, -90, 0))
		#Set up mouse to click buttons again
		self.accept("mouse1", self.buttonPick)
		
	
		
		
		
		
		
	
world = World()  #Creates the world

run()   #Runs the game.