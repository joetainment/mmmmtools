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
import maya.cmds as cmds
import maya.OpenMaya as om
from pymel.all import *
import pymel.all as pm
import maya.mel


## Import the MmmmTools Utils
## this seems to be getting it from the Module Object not the folder
import UtilsMod



try:
    reload( GamerFbxExporter )
except:
    pass
import GamerFbxExporter

U = UtilsMod.Utils

class Gamer(object):
    def __init__(self, parent):
        self.parent = parent
        self.mmmm = self.mmmmTools = self.parent
        self.fbxExporter = GamerFbxExporter.GamerFbxExporter( self.mmmm )
        

    def makeAndParentUcx(self):
        originalSelection = pm.ls(selection=True)
        ## Only attempt to export directly from transform nodes!
        objs = pm.ls( selection=True, transforms=True )
        
        parentObj = objs.pop( )
        
        for i, obj in enumerate(objs):
            newName = 'UCX_' + parentObj.name() + '_' + str(i).zfill(2)
            pm.parent( obj, parentObj )
            obj.rename( newName )
            
            s = obj.getShape()
            s.overrideEnabled.set(True)
            s.overrideShading.set(False)
        
        pm.select( originalSelection)

     
     
    def runGamerMakeAndParentUcx(self):
        reload( GamerFbxExporter )
        #self.fbxExporter = GamerFbxExporter.GamerFbxExporter( self.mmmm )
        self.makeAndParentUcx( )   
        
                
     
    def runGamerAddAttributesForExport(self):
        print( "Gamer.runGamerAddAttributesForExport")
        reload( GamerFbxExporter )
        self.fbxExporter = GamerFbxExporter.GamerFbxExporter( self.mmmm )
        self.fbxExporter.addAttributesForExport( )     
    def runGamerAddAttributeForExportFile(self):
        reload( GamerFbxExporter )
        self.fbxExporter = GamerFbxExporter.GamerFbxExporter( self.mmmm )
        self.fbxExporter.addAttributeForExportFile( )
    def runGamerAddAttributeForExportPath(self):
        reload( GamerFbxExporter )
        self.fbxExporter = GamerFbxExporter.GamerFbxExporter( self.mmmm )
        self.fbxExporter.addAttributeForExportPath( )  
              
              
    def runGamerFbxExportSelection(self):
        reload( GamerFbxExporter )
        self.fbxExporter = GamerFbxExporter.GamerFbxExporter( self.mmmm )
        self.fbxExporter.exportSelection( )
        
    def runGamerFbxExportAll(self):
        reload( GamerFbxExporter )
        self.fbxExporter = GamerFbxExporter.GamerFbxExporter( self.mmmm )
        self.fbxExporter.exportAll( )  
        

        
        
    
    """
    def runSelector( self, makeUi=False, trisOnly=False, ngonsOnly=False, quadsOnly=False ):
        reload( ModelerSelector )
        self.modelerMeshUtilitiesAndAlignerSelector = ModelerSelector.ModelerSelector( makeUi=makeUi, trisOnly=trisOnly, ngonsOnly=ngonsOnly, quadsOnly=quadsOnly )                  
    def runRetoper( self, makeUi=False ):
        reload( ModelerRetoper )
        self.retoper = ModelerRetoper.ModelerRetoper( makeUi=makeUi )  
    def runAligner( self, makeUi=True ):
        reload( ModelerAligner )
        self.modelerAligner = ModelerAligner.ModelerAligner( makeUi=makeUi )
    def runMirrorer( self, makeUi=True ):
        reload( ModelerMirrorer )
        self.modelerMirrorer = ModelerMirrorer.ModelerMirrorer( makeUi=makeUi )
    def runGridTools( self, makeUi=True ):
        reload( ModelerGridTools )
        self.modelerGridTools = ModelerGridTools.ModelerGridTools( parent=self, makeUi=makeUi )
    """