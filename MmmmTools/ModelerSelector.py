## MmmmTools   -  Usability Improvements For Maya
## Copyright (C) <2008>  Joseph Crawford
##  (This file also contains portions written by David Kenley, licensed under the same license.)
##   the primary functionality of this tool was first developed by David Kenley.  It has been adapted
##   for use in MmmmTools with permission from David.
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
import maya.cmds as cmds
import maya.mel as mel
import pymel.all as pm
import math,sys,os
from pymel.all import *


class ModelerSelector(object ):
  def __init__(self, makeUi=False, ngonsOnly=False, trisOnly=False, quadsOnly=False ):
      if makeUi==True:
          self.ui = ModelerSelectorUi( self )
      else:
          self.highlightPolys( trisOnly=trisOnly, ngonsOnly=ngonsOnly, quadsOnly=quadsOnly )

  def highlightTris( self ):
    self.highlightPolys( trisOnly=True )
    
  def highlightNgons( self ):
    self.highlightPolys( ngonsOnly=True )
    
  def highlightQuads( self ):
    self.highlightPolys( ngonsOnly=True )

  def highlightPolys(self, trisOnly=False, ngonsOnly=False, quadsOnly=False):
    import math, sys, os
    import maya.cmds as cmds
    import maya.mel as mel  

    faceWarningList = [];
    triWarningList = [];
    ngonWarningList = [];
    quadWarningList = [];
    originalObject = cmds.ls(selection=True)
    ##Convert selection to faces
    selectedFaces = (cmds.polyListComponentConversion( (cmds.ls (sl=1, flatten=1)), tf=True))
    #print(selectedFaces)
    cmds.select (selectedFaces)

    #make list of selected faces
    selectedItems = (cmds.ls (flatten=True, selection=True))
    lengthOfList = len(selectedItems)
    #print ("***Number of items in list " + str(lengthOfList))
    #print(selectedItems)

    for i in xrange(len(selectedItems)):
        tempFace  = selectedItems[i]
        cmds.select (tempFace)
        #print(tempFace)
        originalSelection = cmds.ls (sl=1, flatten=1)
        #print(type(originalSelection))
        faceVertices = (cmds.polyListComponentConversion( originalSelection, tv=True) )
        cmds.select( faceVertices )
        faceVerticesFlat = cmds.ls(faceVertices, flatten = True)
        cmds.select( originalSelection )

        #print (faceVerticesFlat)
        #print (selectedVertices)
        noOfVertices = 0
        for j in xrange(len(faceVerticesFlat)):
            noOfVertices = 1 + noOfVertices
            #print(noOfVertices)

        if (noOfVertices != 4):
            faceWarningList.append(selectedItems[i])
            
        if (noOfVertices == 3):
            triWarningList.append(selectedItems[i])
        if (noOfVertices == 4):
            quadWarningList.append(selectedItems[i])
        if (noOfVertices > 4):
            ngonWarningList.append(selectedItems[i])
    
    #DisplayResult

    print("Number of Non-Quad Faces Found: " + str(len(faceWarningList)))
    try:
      self.ui.triFace.setValue(len(triWarningList))
      self.ui.ngonFace.setValue(len(ngonWarningList))
    except Exception, e:  ##This will happen if there is no UI
      print( e )
      print("Number of trianges: " + str( len(triWarningList) )    )
      print("Number of ngons: " + str( len(ngonWarningList) )    )
      print("Number of quads: " + str( len(quadWarningList) )    )
    
    if  ngonsOnly:
        if len(ngonWarningList) > 0:
            pm.select(ngonWarningList)
        else:
            pm.select(clear=True, hi = True)
            #pm.select(originalObject, hi = True)
    elif  trisOnly:
        if len(triWarningList) > 0:
            pm.select(triWarningList)
        else:
            pm.select(clear=True, hi = True)
            #pm.select(originalObject, hi = True)
    elif  quadsOnly:
        if len(quadWarningList) > 0:
            pm.select(quadWarningList)
        else:
            pm.select(clear=True, hi = True)
            #pm.select(originalObject, hi = True)
    else:
        if len(faceWarningList) > 0:
            pm.select(faceWarningList)
        else:
            pm.select(clear=True, hi = True)
            #pm.select(originalObject, hi = True)
            
   
    hilite(originalObject)

class ModelerSelectorUi(object):
  def __init__(self, parentRef):
    self.parentRef = parentRef
    self.buttons = []
    self.window = pm.window( sizeable = False, title = "Selector", titleBar=True)
    with self.window:
        self.layout = pm.columnLayout()
        with self.layout:
            self.labFace = pm.text( label='A Useful Tool For Making Selections.', align='left',parent = self.layout )
            self.labFace = pm.text( label='Currently this tool only selects non quad faces.', align='left',parent = self.layout )
            self.labFace3 = pm.text( label='More features will be added to this tool in the future.', align='left',parent = self.layout )

            self.labFace4Blank = pm.text( label='           ', align='left',parent = self.layout )
            self.labFace4Blank = pm.text( label='           ', align='left',parent = self.layout )
            
            btn__find_non_quad_faces = pm.button ( label = 'Find-Quad Face Faces',parent = self.layout,
                        command = lambda xc: self.parentRef.highlightNonQuads(),width = 300  )
            self.buttons.append( btn__find_non_quad_faces )
            
            self.labTriResult = pm.text( label='Number of Triangles Found:', align='left', parent = self.layout )
            self.triFace = pm.intField(parent = self.layout, width = 40,value=0)
            self.labngonResult = pm.text( label='Number of n-Gons Found:', align='left', parent = self.layout )            
            self.ngonFace = pm.intField(parent = self.layout, width = 40,value=0)

            
    # Set the values?
    
    self.buttons.append( btn__find_non_quad_faces )                
    #pm.formLayout( form, edit=True,attachForm=[(self.labVtx,'top',10),(self.labVtx,'left',5),(self.layoutGrid,'top',30),(self.layoutGrid,'left',5),(self.labFace,'top',200),(self.labFace,'left',5),(btn_Face,'top',220),(btn_Face,'left',5),(self.labTriResult,'top',255),(self.labTriResult,'left',5),(self.triFace,'top',250),(self.triFace,'left',160),(self.ngonFace,'top',270),(self.ngonFace,'left',160),(self.labngonResult,'top',275),(self.labngonResult,'left',5)])
    
    # Show Window
    pm.showWindow(self.window)
    self.window.setWidth(600)
    self.window.setHeight(400)