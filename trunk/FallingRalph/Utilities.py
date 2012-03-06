'''###########################################################################################################################
### File: Utilities.py
### Name: Patrick Delaney
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
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import *
from math import sin, cos, pi,sqrt
from random import randint, choice, random
import cPickle, sys

#############METHODS USED FROM TUT-ASTEROIDS###############################################################################
#This helps reduce the amount of code used by loading objects, since all of the
#objects are pretty much the same.
def loadObject(tex = None, pos = Point2(0,0), depth = 0, scale = 15, transparency = True):
  obj = loader.loadModelCopy("plane") #Every object uses the plane model
  obj.reparentTo(render)              
  obj.setPos(Vec3(pos.getX(), pos.getY(), depth)) #Set initial position
  obj.setHpr(Vec3(0, -90, 0))          # -90 since egg file is Y-Up format
  obj.setScale(scale)                 #Set initial scale
  obj.setBin("unsorted", 0)           #This tells Panda not to worry about the
                                      #order this is drawn in. (it prevents an
                                      #effect known as z-fighting)
  obj.setDepthTest(True )             #Tells panda not to check if something
                                      #has already drawn in front of it
                                      #(Everything in this game is at the same
                                      #depth anyway)
  if transparency: obj.setTransparency(1) #All of our objects are trasnparent
  if tex:
    tex = loader.loadTexture("textures/"+tex+".png") #Load the texture
    obj.setTexture(tex, 1)                           #Set the texture

  return obj
def setVelocity(obj, val):
  list = [val[0], val[1], val[2]]
  obj.setTag("velocity", cPickle.dumps(list))
def getVelocity(obj):
  list = cPickle.loads(obj.getTag("velocity"))
  return Vec3(list[0], list[1], list[2])
def genLabelText(text, i):
  return OnscreenText(text = text, pos = (-1.25, .95-.05*i), fg=(1,0.3,0.3,1),
                      align = TextNode.ALeft, scale = .05)
##############################END METHODS USED FROM TUT-ASTEROIDS###################################################
'''
### Name: reflection
### Author: Dr.Zmuda (Modifed by Patrick Delaney, I wasn't sure if my reflection code was wrong, so I used the solution from the
###						s drive)
### Parameters: wallEndPt1 - First endpoint of the wall, wallEndPt2 - second endpoint of the wall, 
###				projectileStartingPt - Starting point of the projectile, 
###				projectileIntersectionPt - where the projectile hits the wall 
### Description: Computes the reflection of the projectile with a wall and returns the reflection vector
'''
def reflection(wallEndPt1, wallEndPt2, projectileStartingPt, projectileIntersectionPt):
	wallVec = wallEndPt1 - wallEndPt2
	n = Vec2(-wallVec[1], wallVec[0])
	n.normalize()
	v = projectileStartingPt - projectileIntersectionPt
	r = n * 2 * v.dot(n) - v
	r.normalize()
	return r
'''
### Name: distance
### Author: Patrick Delaney
### Parameters: objOne - objectOne, objTwo - objectTwo
### Description: Computes the distance between two objects in the xy plane.
'''
def distance(objOne,objTwo):
	return sqrt( (objTwo[1] - objOne[1])**2 + (objTwo[0] - objOne[0])**2)
'''
### Name: setHits
### Author: Patrick Delaney
### Parameters: obj - brick, val - value to set the hits at
### Description: Sets the amount of hits a brick can take
'''
def setHits(obj,val):
	obj.setTag("hits", cPickle.dumps(val))
'''
### Name: getHits
### Author: Patrick Delaney
### Parameters: obj - brick
### Description: Returns the amount of hits a brick has left
'''
def getHits(obj):
	return cPickle.loads(obj.getTag("hits"))
'''
### Name: genLabelText2
### Author: Patrick Delaney
### Parameters: text - String to be displayed, x - xPos, y - yPos
### Description:  Displays the string inputted on the screen at the x and y position. 
'''
def genLabelText2(text, x,y):
  return OnscreenText(text = text, pos = (x,y), fg=(1,0.3,0.3,1),
                      align = TextNode.ALeft, scale = .1)
