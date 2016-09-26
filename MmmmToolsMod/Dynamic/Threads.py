## MmmmTools   -  Usability Improvements For Maya
## Copyright (C) <2008>  Joseph Crawford
##
## This file is part of MmmmTools.
##
## MmmmTools is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## MmmmTools is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
################################################
## More information is available:
## MmmmTools website - http://celestinestudios.com/mmmmtools
################################################



## This module is highly incomplete and experimental.  It should not be
##   enabled in MmmmTools by default




import sys, os, thread, time

import maya.cmds as cmds
import maya.mel
import maya.utils

from Utils import Utils
from Utils import Pather

u = U = Utils



class TimerThread(object):
	def __init__(self, parent):
		self.parent = parent
		nothing = 0
		self.counter = 1
		self.runThread = 0
		self.mmmmTools = self.parent.mmmmTools
		self.conf = self.mmmmTools.conf
	
	def initializeFully(self):
		self.isInitialized = 1
		if self.conf.threads_run_at_start == 1:
			self.runThread = 1
	
	def run(self):
		try:
			test = self.isInitialized
		except:
			self.initializeFully()
		
		self.runCallToMaya()
	
	def runCallToMaya(self):
		while self.runThread == 1:
			try:
				#if self.parent.parent.runPrint == 1:
				maya.utils.executeInMainThreadWithResult( self.runMayaTasks )
				time.sleep(0.1)
				
			except:
				pass
				
	def runMayaTasks(self):
		t = time.clock()
		if t > ( self.timeList[0] + 5*60 )  :   #this needs to get added into a proper conf setting
			self.timeList.insert(  0, t  )
			self.mmmmTools.autoback.saveAutoback()
			#if self.timesDict["autosave_last_time"] < t - self.time
			
			

	
class Threads(object):
	def __init__(self, parent):
		self.parent = parent
		self.mmmmTools = self.parent
		self.timerThread = TimerThread(self)
		thread.start_new_thread(  self.timerThread.run, ()  )