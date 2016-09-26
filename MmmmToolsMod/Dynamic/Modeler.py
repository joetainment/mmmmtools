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
##
## Center Pivot On Component Selection Originally Written by Kert Saville
##
################################################
import math, sys, os
import traceback

import maya.cmds as cmds
import maya.OpenMaya as om
from pymel.all import *
import pymel.all as pm
import maya.mel


import UtilsMod


try:
    reload( ModelerSelector )
except:
    pass
import ModelerSelector

try:
    reload( ModelerMirrorer )
except:
    pass
import ModelerMirrorer

try:
    reload( ModelerRetoper )
except:
    pass
import ModelerRetoper

try:
    reload( ModelerMrClean )
except:
    pass
import ModelerMrClean

try:
    reload( ModelerAligner )
except:
    pass
import ModelerAligner

try:
    reload( ModelerGridTools )
except:
    pass
import ModelerGridTools
U = Utils = UtilsMod.Utils
class Modeler(object):
    def __init__(self, parent):
        self.parent = parent
        
    def creaseSelectedEdges( self ):
        U.creaseSelectedEdges()
                
    def uncreaseSelectedEdges( self ):
        U.uncreaseSelectedEdges()
                
    def selectCreasedEdges( self ):
        U.convertSelectionToCreasedEdges()
            

    def selectHardEdges( self ):
        U.convertSelectionToHardEdges()
        
    def activateSplitPolygonTool( self ):
        pm.mel.eval("SplitPolygonTool;")
          
    def propagateEdgeHardnessOn( self ):
        U.setAttributeOnSelected( "propagateEdgeHardness", 1 )
    
                
    def propagateEdgeHardnessOff( self ):
        U.setAttributeOnSelected( "propagateEdgeHardness", 0 )    
                
    def centerPivotOnComponents(self):
        U.centerPivotOnSelectedComponents()
                
    def runSelector( self, makeUi=False, trisOnly=False, ngonsOnly=False, quadsOnly=False ):
        reload( ModelerSelector )
        self.modelerMeshUtilitiesAndAlignerSelector = ModelerSelector.ModelerSelector( makeUi=makeUi, trisOnly=trisOnly, ngonsOnly=ngonsOnly, quadsOnly=quadsOnly )  

    def pivotToZeroDeleteHistoryAndFreezeTransformsInWorldSpace(self):

        original_selection = pm.ls(selection = True)
        objs = original_selection[:]

        for obj in objs:
            try:
                previous_parent = obj.getParent()
                pm.parent( obj, world=True )                
                pm.move ( obj.scalePivot , [0,0,0] )
                pm.move ( obj.rotatePivot , [0,0,0] )
                pm.makeIdentity (obj, apply = True, normal = 0, preserveNormals = True )
                pm.delete (ch = True )
                pm.parent( obj, previous_parent )                
            except:
                print( traceback.format_exc()     )

        
    def runRetoper( self, makeUi=False ):
        reload( ModelerRetoper )
        self.retoper = ModelerRetoper.ModelerRetoper( makeUi=makeUi )  
    def runAligner( self, makeUi=True ):
        reload( ModelerAligner )
        self.modelerAligner = ModelerAligner.ModelerAligner( makeUi=makeUi )
    def runMirrorer( self, makeUi=True ):
        reload( ModelerMirrorer )
        self.modelerMirrorer = ModelerMirrorer.ModelerMirrorer( makeUi=makeUi )
    def runMrClean( self, makeUi=True ):
        reload( ModelerMrClean )
        self.modelerMrClean = ModelerMrClean.ModelerMrCleanUi( makeUi=makeUi )
    def runGridTools( self, makeUi=True ):
        reload( ModelerGridTools )
        self.modelerGridTools = ModelerGridTools.ModelerGridTools( parent=self, makeUi=makeUi )
