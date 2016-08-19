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


class RendererLightsMultiplier(object ):
    def __init__(self, makeUi=False, selection=False, multiplier = 1.0 ):
        if makeUi==True:
            self.ui = RendererLightsMultiplierUi( self, selection=selection, multiplier=multiplier )
        else:
            self.applyMultiplier(selection=selection, multiplier=multiplier )
    
    def applyMultiplier(self, selection=False, multiplier = 1.0 ):
        originalSelection = pm.ls(selection=True)
        pm.select( hierarchy=True )
        lights = pm.ls(selection=selection, lights=True)
        for light in lights:
            try:
                v = light.intensity.get() * multiplier
                light.intensity.set( v )
            except:
                print( "Coundn't set intensity on light: " + light.name()  )
        pm.select(originalSelection)
        
    

class RendererLightsMultiplierUi(object):
  def __init__(self, parentRef, selection=False, multiplier=1.0):
    self.parentRef = parentRef
    self.buttons = []
    self.window = pm.window( sizeable = False, title = "Light Multiplier", titleBar=True)
    with self.window:
        self.layout = pm.columnLayout()
        with self.layout:  ## Using Ui on the end of Widget names
            self.multiplierText = pm.text( label='Multiplier:', align='left' )
            self.multiplierUi = pm.floatField( value=1.0 )
            self.checkBoxUi = pm.checkBox( label='Affect Selected Lights Only')
            self.okUi = pm.button ( label = 'Apply',parent = self.layout,
                        command = lambda xc: self.parentRef.applyMultiplier( multiplier=self.multiplierUi.getValue(),
                                    selection=self.checkBoxUi.getValue(),
                                ),
                        width = 300  )
    pm.showWindow(self.window)
    self.window.setWidth(600)
    self.window.setHeight(400)
    
    
    
    
    
    
    
    
pass