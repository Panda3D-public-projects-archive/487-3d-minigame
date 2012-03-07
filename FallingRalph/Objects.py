'''###########################################################################################################################
### File: Objects.py
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

#####CONSTANTS######

class Objects:
	
	#Once we determine what objects we want to use - I will modify the constructor here. It will be similar to the player 
	#Constructor - Patrick
	'''
	### Name: 
	### Author: Patrick Delaney
	### Parameters: 
	### Description: 
	'''
	def __init__(self,type):
		if(type == 1):
			print "stuff"
	