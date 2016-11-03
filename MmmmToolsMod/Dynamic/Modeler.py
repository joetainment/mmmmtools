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

import MmmmToolsMod



modules_to_import = [
'UtilsMod',
'ModelerSelector',
'ModelerMirrorer',
'ModelerRetoper',
'ModelerMrClean',
'ModelerGridTools',
'ModelerAligner',
]
importCode = """
try:
    *module*=*module*
    ## if we get this far, then the module must exist, and we should reload it
    try:
        reload(*module*)
    except:
        ## in this case, the reload fails, so print the traceback
        print( traceback.format_exc() )
    
except:
    ## in this case, *module* has never been loaded before
    try:
        import *module*
    except:
        ## in this case, the import fails, so print the traceback
        print( traceback.format_exc() )
"""
for m in modules_to_import:
    exec( importCode.replace('*module*', m ) , globals(), locals() )

class Modeler(object):
    def __init__(self, parent):
        self.parent = parent
        
        self.mmmm = self.parent
        self.addToCommander()
        
    def addToCommander(self):
        commander = self.mmmm.commander
        
        inMenu = 'Modeler'  
        
        commander.addCommand(
            'Modeler/ActivateSplitPolygonTool',
            MmmmToolsMod.Static.Mesh.activateSplitPolygonTool,
            uiLabel='Split Polygon Tool',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/CreaseSelectedEdges',
            MmmmToolsMod.Static.Mesh.creaseSelectedEdges,
            uiLabel='Crease Selected Edges',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/UncreaseSelectedEdges',
            MmmmToolsMod.Static.Mesh.uncreaseSelectedEdges,
            uiLabel='Uncrease Selected Edges',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/ConvertSelectionToCreasedEdges',
            MmmmToolsMod.Static.Mesh.convertSelectionToCreasedEdges,
            uiLabel='Convert Selection To Creased Edges',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/ConvertSelectionToHardEdges',
            MmmmToolsMod.Static.Mesh.convertSelectionToHardEdges,
            uiLabel='Convert Selection To Hard Edges',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/PropagateEdgeHardnessOn',
            lambda: MmmmToolsMod.Static.Mesh.\
                setAttributeOnSelected( "propagateEdgeHardness", 1 ),
            uiLabel='Propagate Edge Hardness On',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/PropagateEdgeHardnessOff',
            lambda: MmmmToolsMod.Static.Mesh.\
                setAttributeOnSelected( "propagateEdgeHardness", 0 ),
            uiLabel='Propagate Edge Hardness Off',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/PivotToZeroDeleteHistoryAndFreezeTransformsInWorldSpace',
            MmmmToolsMod.Static.Mesh.\
            pivotToZeroDeleteHistoryAndFreezeTransformsInWorldSpace,
            uiLabel='Pivot To Zero \n DeleteHistory \n Freeze Transforms \n In World Space',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/SelectNonQuads',
            self.selectNonQuads,
            uiLabel='SelectNonQuads',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/SelectTris',
            self.selectTris,
            uiLabel='SelectNonTris',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/SelectNgons',
            self.selectNgons,
            uiLabel='SelectNonNgons',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/SelectQuads',
            self.selectQuads,
            uiLabel='SelectQuads',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/CenterPivotOnSelectedComponents',
            MmmmToolsMod.Static.Mesh.centerPivotOnSelectedComponents,
            uiLabel='Center Pivot On Selected Components',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/VertexAligner',
            self.runAligner,
            uiLabel='Vertex Aligner...',
            inMenu=inMenu,
        )
        commander.addCommand(
            'Modeler/MrClean',
            self.runMrClean,
            uiLabel='Mr. Clean...',
            inMenu=inMenu,            
        )
        commander.addCommand(
            'Modeler/MenuEntryFromCommanderFunc',
            self.menuEntryFromCommanderFunc,
            uiLabel='Experimental Command',
            inMenu='Developer'
        )
    def menuEntryFromCommanderFunc(self):
        print( "Experiment Command")
        
    
    def selectNonQuads( self ):
        self.runSelector( makeUi = False )
    def selectTris( self ):
        self.runSelector( makeUi = False, trisOnly=True )
    def selectNgons( self ):
        self.runSelector( makeUi = False, ngonsOnly=True )
    def selectQuads( self ):
        self.runSelector( makeUi = False, quadsOnly=True )

    def pivotToZeroDeleteHistoryAndFreezeTransformsInWorldSpace(self):
        tmp = MmmmToolsMod.Static.Mesh
        tmp.pivotToZeroDeleteHistoryAndFreezeTransformsInWorldSpace();
        
    def runSelector( self, makeUi=False, trisOnly=False, ngonsOnly=False, quadsOnly=False ):
        reload( ModelerSelector )
        self.modelerMeshUtilitiesAndAlignerSelector = ModelerSelector.ModelerSelector( makeUi=makeUi, trisOnly=trisOnly, ngonsOnly=ngonsOnly, quadsOnly=quadsOnly )  
 
    def runRetoper( self, makeUi=False, parentWidget=None ):
        reload( ModelerRetoper )
        self.retoper = ModelerRetoper.ModelerRetoper( makeUi=makeUi, parentWidget=parentWidget )  
    def runAligner( self, makeUi=True ):
        reload( ModelerAligner )
        self.modelerAligner = ModelerAligner.ModelerAligner( makeUi=makeUi )
    def runMirrorer( self, makeUi=True, parentWidget=None ):
        reload( ModelerMirrorer )
        self.modelerMirrorer = ModelerMirrorer.ModelerMirrorer( makeUi=makeUi, parentWidget=parentWidget )
    def runMrClean( self, makeUi=True ):
        reload( ModelerMrClean )
        self.modelerMrClean = ModelerMrClean.ModelerMrCleanUi( makeUi=makeUi )
    def runGridTools( self, makeUi=True, parentWidget=None ):
        reload( ModelerGridTools )
        self.modelerGridTools = ModelerGridTools.ModelerGridTools( parent=self, makeUi=makeUi, parentWidget=parentWidget )

        
    #### DeprecationWarning - use version in Static              
    def centerPivotOnComponents(self):
        MmmmToolsMod.Static.Mesh.centerPivotOnSelectedComponents()      
    #### DeprecationWarning - use version in Static            
    def creaseSelectedEdges( self ):
        MmmmToolsMod.Static.Mesh.creaseSelectedEdges()
    #### DeprecationWarning - use version in Static                    
    def uncreaseSelectedEdges( self ):
        MmmmToolsMod.Static.Mesh.uncreaseSelectedEdges()
    #### DeprecationWarning - use version in Static                    
    def selectCreasedEdges( self ):
        MmmmToolsMod.Static.Mesh.convertSelectionToCreasedEdges()
            
    #### DeprecationWarning - use version in Static        
    def selectHardEdges( self ):
        MmmmToolsMod.Static.Mesh.convertSelectionToHardEdges()
    #### DeprecationWarning - use version in Static            
    def activateSplitPolygonTool( self ):
        pm.mel.eval("SplitPolygonTool;")
    #### DeprecationWarning - use version in Static                  
    def propagateEdgeHardnessOn( self ):
        UtilsMod.Utils.setAttributeOnSelected( "propagateEdgeHardness", 1 )
    #### DeprecationWarning - use version in Static        
    def propagateEdgeHardnessOff( self ):
        UtilsMod.Utils.setAttributeOnSelected( "propagateEdgeHardness", 0 )    
                  