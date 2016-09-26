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
import pymel.all as pm

import maya.OpenMaya as OpenMaya

from . import TexturerUvXformsTool


class Texturer(object):
    def __init__(self,parentRef):
        self.parentRef = parentRef
        self.mmmmTools = self.parentRef
        self.conf = self.mmmmTools.configuration.conf
        self.seamsHiddenString="unknown"
        self.ratioOfUvsToWorldArea = 0.0001
        
    def reloadTextures(self):
        print("Reloading textures for selected objects.")
        try:
            self.mmmmTools.fileTextureReloader.reload()
        except:
            traceback.print_exc()    
        pass
    
    def selectTextureBorderEdges(self):
        print("Selecting seams (texture border edges).")
        try:
            self.mmmmTools.selectTextureBorderEdges.selectTextureBorderEdges()
        except:
            traceback.print_exc()

    
    def selectSeams(self):
        self.selectTextureBorderEdges()
    
    def toggleSeams(self):
        print( "Toggling visibility of seams.")
        if self.seamsHiddenString!="showing":
            self.showSeams()
            self.seamsHiddenString = "showing"
        else:
            self.hideSeams()        
            self.seamsHiddenString = "hidden"
    
    def showSeams(self):
        print( 'Showing seams.'  )
        pm.polyOptions( displayMapBorder=True, gl=True ) ## gl for global
        pm.polyOptions( sizeBorder=self.conf.texturer_show_seams_border_thickness,
                        gl=True ) ## gl for global
    
    def hideSeams(self):
        print( 'Hiding seams.'  )
        pm.polyOptions( displayMapBorder=False, gl=True ) ## gl for global
        
    def runUvXformsTool(self):
        self.uvXformsTool = TexturerUvXformsTool.TexturerUvXformsTool(self, auto_ui=True)
    

    def calcUvToWorldAreaRatio(self):
        oSel = pm.ls(sl=True)

        pm.mel.eval( "ConvertSelectionToFaces;" )
        sel = pm.ls(sl=True)
        
        worldAreaTotal = 0.0
        uvAreaTotal = 0.0
        tmpList = [None]
        singleList = [None]
        cmpsList = []
        
        for entry in sel:
                    # print entry   #3print type(entry)   # print help(type(entry) ) # print( len(entry)  )
            ## MeshFace Objects can be multiples, so they themselves are iterable!
            for subEntry in entry:
                uvAreaTotal += subEntry.getUVArea( )
                worldAreaTotal += subEntry.getArea( 'world' )  ## world is one of the available spaces
        
        ratioOfUvsToWorldArea = uvAreaTotal / worldAreaTotal
        
        pm.select( oSel )
        return ratioOfUvsToWorldArea
    
    
    def grabUvToWorldRatioOfSelection( self ):
        self.ratioOfUvsToWorldArea = self.calcUvToWorldAreaRatio()
        self.displayInfoUvToWorldRatioAsMsg()

    def displayInfoUvToWorldRatioAsMsg( self ):
        OpenMaya.MGlobal.displayInfo(  str(self.ratioOfUvsToWorldArea)  )    
    
    def applyGrabbedUvToWorldRatioToSelection( self ):
        targetRatio = self.ratioOfUvsToWorldArea
        self.applyUvToWorldRatioToSelection( targetRatio = self.ratioOfUvsToWorldArea )

    def applyNumericalUvToWorldRatioToSelection( self ):
        targetRatio = input()
        self.applyUvToWorldRatioToSelection( targetRatio = targetRatio )
    
        
    def applyUvToWorldRatioToSelection( self, targetRatio=None ):
        oSel = pm.ls(sl=True)

        pm.mel.eval( "ConvertSelectionToFaces;" )
        
        sel = pm.ls(sl=True)       
        
        if targetRatio == None:
            targetRatio = input()
        currentRatio = self.calcUvToWorldAreaRatio()
        amountToScaleBeforeSqrt = targetRatio / currentRatio
        amountToScale = math.sqrt( amountToScaleBeforeSqrt )
        
        ## Calc a bounding box in uv space, and it's center, for a scale pivot
        bb = pm.polyEvaluate( sel, boundingBoxComponent2d=True )
        bbUMin = bb[0][0]
        bbUMax = bb[0][1]
        bbVMin = bb[1][0]
        bbVMax = bb[1][1]
        bbUCenter = (bbUMax + bbUMin) * 0.5
        bbVCenter = (bbVMax + bbVMin) * 0.5
        
        pm.polyEditUV( sel, pu=bbUCenter, pv=bbVCenter, su = amountToScale, sv = amountToScale )
        
        pm.select( oSel )        
    
    
    def unfold3dMultipleObjects(self):
        origSel = pm.ls(selection=True)
        for obj in origSel:
            pm.select(obj)
            pm.mel.eval( "ConvertSelectionToUVs;" )
            pm.mel.eval( "Unfold3D -unfold -iterations 1 -p 1 -borderintersection 1 -triangleflip 1;" )
        pm.select( origSel )

    
    def unfold3dOnlySelected(self):

        origSel = pm.ls(selection=True)

        pm.mel.eval( "PolySelectConvert 4;" )  ##"ConvertSelectionToUVs;" )
        origUvs = pm.ls(selection=True)
        pm.mel.eval( "InvertSelection;" )

        selCount = len( pm.ls(selection=True) )
        
        ## In case all uvs are selected, the inverted selection will be zero!
        if selCount==0:
            pm.select( origSel )
            pm.mel.eval( "ConvertSelectionToUVs;" )
            pm.mel.eval( "Unfold3D -unfold -iterations 1 -p 1 -borderintersection 1 -triangleflip 1;" )
            pm.select( origSel )
        else:
            ## Beware!  there's a huge potential bug  in this commands behavior
            ##   the way it is now working here is to get u and v  values, as back to back entries added into a list
            ##   so the list is twice as long as the number of uvs   eg.   v = coords[i*2  +1]
            uvsToRestore = pm.ls(selection=True, flatten=True )            
            coords = pm.polyEditUV(uvsToRestore, query=True, uValue=True, vValue=True)


            pm.select(origSel)
            pm.mel.eval( "ConvertSelectionToUVs;" )
            pm.mel.eval( "Unfold3D -unfold -iterations 1 -p 1 -borderintersection 1 -triangleflip 1;" )
            


            #print( uvsToRestore )
            #print len(coordsU)
            #print len( uvsToRestore )

            #print( coords )

            for i,uv in enumerate(uvsToRestore):
                #print( coords )
                pm.polyEditUV( uv, relative=False, uValue = coords[i*2], vValue=coords[i*2  + 1] )

            #cmds.Unfold3D( cmds.ls(sl=True), u=True, p=True, ite=1, bi=True, tf=True, ms=1024, rs=2 )

            pm.select(origSel)        
    
    def roadkill(self):
        self.runRoadkill()
        
    def runRoadkill(self):
        print( 'Running Roadkill via mel:  "MmmmToolsRoadKill;" ' )
        try:
            pm.mel.eval('MmmmToolsRoadKill;')
        except:
            traceback.print_exc()