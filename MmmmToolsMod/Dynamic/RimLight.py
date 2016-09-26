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


## Thanks to Gabriele Coen, who wrote a mel script which was studied in order to write this one.
## At the time of this writing, his script is available at:
## http://highend3d.com/maya/downloads/mel_scripts/lighting/rimLight-LOL-5190.html


import maya.cmds as cmds


class RimLight(object):
	def __init__(self, parent):
		self.parent = parent
		self.ini = parent.ini
		
	def create(self):
		origName = 'rimLight'
		numberSuffix = 0
		
		if origName in cmds.ls():
			numberSuffix = 1
			while origName+str(numberSuffix) in cmds.ls():
				numberSuffix = numberSuffix + 1
		
		if numberSuffix == 0:
			uniqueName = origName
		else:
			uniqueName = origName+str(numberSuffix)

		cmds.directionalLight(name = uniqueName)
		cmds.select(cl = True)
		if uniqueName == origName:
			shapeName=uniqueName+'Shape'
		else:
			shapeName = origName + 'Shape' + str(numberSuffix)
		cmds.select( shapeName , r = True )
		cmds.addAttr(sn = 'rimIntensity', defaultValue = 1, h = False, k = True)
		cmds.addAttr(sn = 'sensitivity', defaultValue = 0.5, h = False, k = True)
		cmds.addAttr(sn = 'start', defaultValue = 0, h = False, k = True)
		cmds.addAttr(sn = 'end', defaultValue = 1, h = False, k = True)
		cmds.addAttr(sn = 'startIntensity', defaultValue = 3, h = False, k = True)
		cmds.addAttr(sn = 'endIntensity', defaultValue = 0, h = False, k = True)
		
		
		#Create new nodes for shading of light
		remapName = uniqueName + '_remapValue'
		cmds.createNode( 'remapValue', name=remapName )
		samplerName = uniqueName + '_samplerInfo'
		cmds.createNode( 'samplerInfo', name=samplerName )
		
		
		#set attributes of newly created nodes
		cmds.setAttr( remapName + '.value[0].value_FloatValue', 1)
		cmds.setAttr( remapName + '.value[1].value_FloatValue', 0)
		cmds.setAttr( remapName + '.value[0].value_Interp', 2)
		
		
		#connect attributes
		cmds.connectAttr( samplerName+'.normalCameraZ' , remapName+'.inputValue')
		cmds.connectAttr( shapeName+'.startIntensity' , remapName+'.value[0].value_FloatValue')
		cmds.connectAttr( shapeName+'.endIntensity' , remapName+'.value[1].value_FloatValue')
		cmds.connectAttr( shapeName+'.start' , remapName+'.value[0].value_Position')
		cmds.connectAttr( shapeName+'.end' , remapName+'.value[1].value_Position')
		cmds.connectAttr( shapeName+'.rimIntensity' , remapName+'.outputMax')
		cmds.connectAttr( shapeName+'.sensitivity' , remapName+'.inputMax')
		cmds.connectAttr( remapName+'.outValue' , shapeName+'.intensity')
		
		cmds.setAttr( shapeName+'.intensity', keyable = False, channelBox = False )
		
		
		cmds.select( uniqueName, r = True )