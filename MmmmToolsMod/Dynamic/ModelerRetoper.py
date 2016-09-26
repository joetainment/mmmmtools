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
import UtilsMod
Utils = UtilsMod.Utils

class ModelerRetoper(object):
  __instance = None
  referenceXformNode = None
  
  @classmethod
  def clearInstance(cls):
      cls.__instance = None
  
  @classmethod
  def getExistingInstance(cls):
      return cls.__instance 
  
  @classmethod
  def getInstance(cls):
      if not cls.__instance is None:
          return cls.__instance
      else:
          cls.__instance = ModelerRetoper( makeUi=False )
          return cls.__instance

  def __init__(self, makeUi=False, projectImmediately=False, setReferenceImmediately=False ):
      ModelerRetoper.__instance = self
      if makeUi==True:
          self.ui = ModelerRetoperUi( self )
      if projectImmediately==True:
          self.projectSelection()
      if setReferenceImmediately==True:
          self.setReference()

          
  def makeReferenceLive( self ):
      pm.makeLive( self.referenceXformNode )
      
      
  def makeReferenceNotLive( self ):
      pm.makeLive(none=True)
                
  def makeReferenceHidden( self ):
      self.referenceXformNode.visibility.set( False )
      
      
  def makeReferenceVisible( self ):
      self.referenceXformNode.visibility.set( True )
      
      
  def setReference( self ):
    try:
        self.referenceXformNode = pm.ls(selection=True)[-1]
    except:
        print( "Please select at least one object in order to set the retoper reference mesh. ",
        "If multiple objects are selected, the last object will be used." )
    
  def projectSelection( self ):

    hiliteOrig = pm.ls(hilite=True)
  
    selOrig = pm.ls(selection=True)
    selPre = pm.polyListComponentConversion(   selOrig, tv=True  )    
    
    try:
        pm.select( self.referenceXformNode, replace=True )
        pm.select( selPre, add=True )
        selForTransfer = pm.ls(selection=True)
        pm.transferAttributes( transferPositions=1, transferNormals=0,transferUVs=0,transferColors=0, sampleSpace=0, searchMethod=0 )
        objsToAddToSelection = []
        for o in selForTransfer:
        #s = str( type(o) )
        #print "y" + s + "y"
          if str( type(o) ) == "<class 'pymel.core.general.MeshVertex'>":
            n = o.name().split('.')[0]
            objsToAddToSelection.append( n )
        for obj in objsToAddToSelection:
          pm.select( obj, add=True )
        pm.delete( ch = True ) ##was #pm.mel.eval( "DeleteHistory;" )
        print( selForTransfer )
        pm.select( selOrig, replace=True )  
        pm.hilite( hiliteOrig)
    except:
        pm.select( selOrig )
        pm.hilite( hiliteOrig)
        
        print( "Please ensure that you have a valid reference mesh selected, and that you have verticies or objects select to project.")        
    
          


class ModelerRetoperUi(object):
  def __init__(self, parentRef):
    self.parentRef = parentRef
    self.buttons = []
    self.window = pm.window( sizeable = True, title = "Retoper", titleBar=True)
    with self.window:
        self.layout = pm.columnLayout()
        with self.layout:
            self.lab1 = pm.Text( label='A "Retop" Tool For Creating New Topology.', align='left',parent = self.layout )
            self.lab2 = pm.Text( label='Please Note: This tool does not preserve', width=300, align='left',parent = self.layout )
            self.lab3 = pm.Text( label='construction history of edited objects.', width=300, align='left',parent = self.layout )
             

            btn__setReference = pm.Button ( label = 'Set Reference Mesh',parent = self.layout,
                        command = lambda xc: self.parentRef.setReference(),width = 300  )
            self.buttons.append( btn__setReference )
            
            btn__makeReferenceLive = pm.Button ( label = 'Make Reference Live',parent = self.layout,
                        command = lambda xc: self.parentRef.makeReferenceLive(),width = 300  )
            self.buttons.append( btn__makeReferenceLive )
            
            btn__makeReferenceNotLive = pm.Button ( label = 'Make Reference Not Live',parent = self.layout,
                        command = lambda xc: self.parentRef.makeReferenceNotLive(),width = 300  )
            self.buttons.append( btn__makeReferenceNotLive )
                        
            btn__makeReferenceHidden = pm.Button ( label = 'Make Reference Hidden',parent = self.layout,
                        command = lambda xc: self.parentRef.makeReferenceHidden(),width = 300  )
            self.buttons.append( btn__makeReferenceHidden )
            
            btn__makeReferenceVisible = pm.Button ( label = 'Make Reference Visible',parent = self.layout,
                        command = lambda xc: self.parentRef.makeReferenceVisible(),width = 300  )
            self.buttons.append( btn__makeReferenceVisible )
            
            btn__projectSelection = pm.Button ( label = 'Project Selection To Surface',parent = self.layout,
                        command = lambda xc: self.parentRef.projectSelection(),width = 300  )
            self.buttons.append( btn__projectSelection )            
            
            ## put a button here for auto new material and transparency animation
            ## put a button here for auto ref layer
            ## put a button here for quad draw (a shortcut)
            ## put a button here to project along particular axis (essentially just scale first)
            
            
    # Show Window
    pm.showWindow(self.window)
    self.window.setWidth(200)
    self.window.setHeight(300)