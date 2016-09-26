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


class RendererProductionShadersMaker(object ):
    def __init__(self, makeUi=False ):
        self.shaderTypes = [ 'mib_volume',
        'mip_binaryproxy',
        'mip_cameramap',
        'mip_card_opacity',
        'mip_gamma_gain',
        'mip_grayball',
        'mip_matteshadow',
        'mip_matteshadow_mtl',
        'mip_mirrorball',
        'mip_motion_vector',
        'mip_motionblur',
        'mip_rayswitch',
        'mip_rayswitch_advanced',
              'mip_rayswitch_environment',]
        if False:  ##makeUi==True:
            self.ui = RendererProductionShadersMakerUi( self )
        else:
            self.showMipShadersInInterface( )
      
    def showMipShadersInInterface(self):
        mel.eval( 'optionVar -sv "MIP_SHD_EXPOSE" 1;' )
        
        
    ## At the moment, the mip shader maker stuff below isn't called at all because the UI shows them now!!!
    def makeShaders(self, shaderToMake='all'):
        if shaderToMake == 'all':
            for shaderType in self.shaderTypes:
                self.makeShaderWithCreateNode( shaderType )

    def makeShaderWithCreateNode(self, shaderType ):
        # pm.createNode( shaderType )   ## For some reason, the python version of this command does not work with mip shaders... i dunno why...
        ## Use mel to make MIP shaders
        try:
            mel.eval( 'createNode "' + str(shaderType) + '";' )
        except:
            print( 'cannot create shader type:' + str(shaderType)  )        
    
    

class RendererProductionShadersMakerUi(object):
    pass
"""
  def __init__(self, parentRef):
    self.parentRef = parentRef
    self.buttons = []
    self.window = pm.window( sizeable = False, title = "Selector", titleBar=True)
    with self.window:
        self.layout = pm.columnLayout()
        with self.layout:
            self.labFace = pm.text( label='A Useful For Making Selections.', align='left',parent = self.layout )
            self.labFace = pm.text( label='Currently this tool only selects non quad faces.', align='left',parent = self.layout )
            self.labFace3 = pm.text( label='More features will be added to this tool in the future.', align='left',parent = self.layout )

            self.labFace4Blank = pm.text( label='           ', align='left',parent = self.layout )
            self.labFace4Blank = pm.text( label='           ', align='left',parent = self.layout )
            
            btn__find_non_quad_faces = pm.button ( label = 'Find-Quad Face Faces',parent = self.layout,
                        command = lambda xc: self.parentRef.highlightNonQuads(),width = 300  )
            self.buttons.append( btn__find_non_quad_faces )
            
            self.labTriResult = pm.text( label='Number of Triangles Found:', align='left', parent = self.layout )
            self.triFace = pm.intField(parent = self.layout, width = 40,value=0)
            self.labnGonResult = pm.text( label='Number of n-Gons Found:', align='left', parent = self.layout )            
            self.nGonFace = pm.intField(parent = self.layout, width = 40,value=0)

            
    # Set the values?
    
    self.buttons.append( btn__find_non_quad_faces )                
    #pm.formLayout( form, edit=True,attachForm=[(self.labVtx,'top',10),(self.labVtx,'left',5),(self.layoutGrid,'top',30),(self.layoutGrid,'left',5),(self.labFace,'top',200),(self.labFace,'left',5),(btn_Face,'top',220),(btn_Face,'left',5),(self.labTriResult,'top',255),(self.labTriResult,'left',5),(self.triFace,'top',250),(self.triFace,'left',160),(self.nGonFace,'top',270),(self.nGonFace,'left',160),(self.labnGonResult,'top',275),(self.labnGonResult,'left',5)])
    
    # Show Window
    pm.showWindow(self.window)
    self.window.setWidth(600)
    self.window.setHeight(400)
"""