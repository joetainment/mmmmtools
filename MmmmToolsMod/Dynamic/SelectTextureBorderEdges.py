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


## Thanks to the user Rebb,  (real name unknown, but username was from polycount) who
## posted a script that was studied in order to create this one.
## http://boards.polycount.net/showthread.php?t=52722

import maya.cmds as cmds
import maya.mel as mel

class SelectTextureBorderEdges(object):

	def __init__(self,parentRef=None):
		self.parentRef = parentRef
	
	def disableSelectionConstraints(self):
	
		## Haven't been able to find a way to do this in python.  Tried various forms of disabling the   ****
		## constraints as shown in the docs, but the constraints never completely go away.
		mel.eval("PolygonSelectionConstraints;")
		mel.eval("resetPolySelectConstraint;")
		mel.eval("deleteUI polySelectionConstraintPanel1Window;")
		
		
	
	def selectTextureBorderEdges(self):
		#Some notes:
		
		#Turn off the selection constraints
		self.disableSelectionConstraints()
		

		#Grab the selected objects
		objs = cmds.ls(selection=True)

		#Convert those objects to a UV selection and then select it
		uvs = cmds.polyListComponentConversion( objs, toUV=True )
		cmds.select(uvs, r=True)

		#This command contrains the selection to only the UV border, which is basically just deselecting a bunch of other UVs
		cmds.polySelectConstraint(pp=3)
	
		#Get the current selection, which should be a bunch of UVs
		uvShellBorderUvs = cmds.ls(selection=True)   #select(uvs, r=True)
		
		#Convert to edge selection, only selecting edges entirely contained by the UVs, then select it.
		textureBorderEdges = cmds.polyListComponentConversion( uvShellBorderUvs, fromUV=True, toEdge=True, internal=True )
		
		
		cmds.select(textureBorderEdges, r=True)

		## We need to flatter the selection list, otherwise it selects using ranges.
		textureBorderEdges = cmds.ls(textureBorderEdges, fl=True)
		
		testedBorder = []
		
		
		for currentEdge in textureBorderEdges:
			cmds.select(currentEdge, replace=True)
			#print("updated\n")
			edgeUVs=cmds.polyListComponentConversion(currentEdge, tuv=1)
			
			edgeUVs=cmds.ls(edgeUVs, fl=1)
			#print(edgeUVs)
			if len(edgeUVs)>2:
				testedBorder.append(currentEdge)
		
		
		
		#Convert those objects to a UV selection and then select it
		allEdges = cmds.polyListComponentConversion( objs, toEdge=True )
		
		cmds.select(allEdges, r=True)
		
		cmds.polySelectConstraint(m=2,t=int( '0x8000', 16 ),w=1)		
		borderEdges3d = cmds.ls(selection=True, fl=True)
		
		print( borderEdges3d )
		
		
		
		if len(testedBorder) > 0:
			cmds.select(testedBorder, r=True)
		
		if len(borderEdges3d) > 0:
			cmds.select(borderEdges3d, add=True)
		
		cmds.polySelectConstraint( w=0)
        
		## Turn off the selections constraints
		self.disableSelectionConstraints()
