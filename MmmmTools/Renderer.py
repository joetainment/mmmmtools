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
import traceback
from pymel.core import *
import maya.mel
import pymel.all as pm
import RendererProductionShadersMaker
import RendererLightsMultiplier

class Renderer(object):
    def __init__(self, parent):
        self.parent = parent
    
    """         
    def runSelector( self, makeUi=True ):
        reload( ModelerSelector )
        self.modelerMeshUtilitiesAndAlignerSelector = ModelerSelector.ModelerSelector( makeUi=makeUi )  
    def runAligner( self, makeUi=True ):
        reload( ModelerAligner )
        self.modelerAligner = ModelerAligner.ModelerAligner( makeUi=makeUi )"""    

    def reflectivityOfSelectedMaterialsToZero(self):
        objs = pm.ls(selection=True)
        for obj in objs:
            try:
                obj.reflectivity.set(0)
            except:
                print( "Could not set reflectivity for node: " + obj.name()  )
                traceback.print_exc()

    

    def runProductionShadersMaker(self):
        try:
            reload( RendererProductionShadersMaker )
        except:
            import RendererProductionShadersMaker
        self.productionShadersMaker = RendererProductionShadersMaker.RendererProductionShadersMaker( makeUi=True )
        
    def runLightsMultiplier(self):
        try:
            reload( RendererLightsMultiplier )
        except:
            import RendererLightsMultiplier
        self.lightsMultiplier = RendererLightsMultiplier.RendererLightsMultiplier( makeUi=True )
        
        
        
#        RendererLightsMultiplier


    def addVrayTextureInputGammaAttributes(self):
        objs = pm.ls (selection = True)

        for obj in objs:
            try:
                pm.mel.eval( "vray addAttributesFromGroup " + obj.name() + " vray_file_gamma 1;")
            except :
                print( traceback.format_exc() )
                
    def setVrayTextureToSRGB(self ):
        self.setVrayTextureInputGamma( 2 ) ## 0 is for linear mode, 2 is for SRGB
    def setVrayTextureToLinear(self ):
        self.setVrayTextureInputGamma( 0 ) ## 0 is for linear mode, 2 is for SRGB
    
    
    def setVrayTextureInputGamma(self, color_space_enumeration ):
        ## 0 is for linear mode, 2 is for SRGB    
        objs = pm.ls (selection = True)

        for obj in objs:
            try:
                obj.vrayFileColorSpace.set ( color_space_enumeration )
            except :
                print( traceback.format_exc() )
    
    def useOutRInsteadOfAlphaOfConnected(self):
        pass
        
    def vrayStarterSettings(self):
        pass
        
    
    def setHypershadeThumbnailsEnabled( self, enabled=True ):
        if not enabled:
            mel = "renderThumbnailUpdate 0;"
        else:
            mel = "renderThumbnailUpdate 1;"           
        pm.mel.eval(  mel )
        
    def setMipShadersEnabled( self, enabled=True ):
        if not enabled:
            mel = 'optionVar -iv "MIP_SHD_EXPOSE" 0;'
        else:
            mel = 'optionVar -iv "MIP_SHD_EXPOSE" 1;'           
        pm.mel.eval(  mel )
        
        

        