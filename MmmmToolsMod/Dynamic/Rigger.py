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


## Thanks to Gabriele Coen, who wrote a mel script which was studied in order to write this one.
## At the time of this writing, his script is available at:
## http://highend3d.com/maya/downloads/mel_scripts/lighting/rimLight-LOL-5190.html


from pymel.core import *
import pymel.all as pm

"""
#Note: Try this command
rop = mmmmTools.rigger.Rigger( action='constrain' )
"""


import RiggerJointOrientHelper
import RiggerRiveter
import RiggerAttributeSetter as RiggerAttributeSetterModule
import RiggerAttributeConnector as RiggerAttributeConnectorModule

RiggerAttributeSetter = RiggerAttributeSetterModule.RiggerAttributeSetter
RiggerAttributeConnector = RiggerAttributeConnectorModule.RiggerAttributeConnector

from . import RenameByRegex



class Rigger(object):
    def __init__(self, parentGiven, action='default'):
        self.parent = parentGiven
        self.action = action
    
    def moveUpInHierarchy( self ):
        self.parent.utils.moveUpInHierarchy()
    
    def callAction(self, isPreparationNeeded=True, action=''):
        if not (action == ''):
            self.action = action
        if isPreparationNeeded:
            self.prepareForOperation()
        try:
            self[ self.action ].call( self )
        except:
            print "Please specify an action"        

    def prepareForOperation(self):
        self.objs = ls(selection=True)
        self.zeros = {}
        self.objA = self.objs[0]
        try:
            self.objB = self.objs[1]
        except:
            pass
            
    def align(self, isPreparationNeeded=True):
        if isPreparationNeeded:
            self.prepareForOperation()
        try:
            assert( len(self.objs) == 2 )   
            constraints= []
            constraints.append(\
                pointConstraint( self.objB, self.objA ) )
            constraints.append(\
                orientConstraint( self.objB, self.objA ) )
            constraints.append(\
                scaleConstraint( self.objB, self.objA ) )
            for c in constraints:
                delete( c )
        
        except:
            "Please Select 2 Objects"
            
    def alignObjAToObjB( self, objA, objB, objs=None, originalSelection=None  ):
        if originalSelection==None:
            originalSelection=ls(selection=True)
        constraints= []
        constraints.append(
            pointConstraint( objB, objA ) )
        constraints.append(
            orientConstraint( objB, objA ) )
        constraints.append(
            scaleConstraint( objB, objA ) )
        for c in constraints:
            delete( c )
        
        select( originalSelection )
        
                
                
    def constrain(self, isPreparationNeeded=True):
        if isPreparationNeeded:
            self.prepareForOperation()
        try:
            assert( len(self.objs) == 2 )
            constraints= []
            constraints.append(\
                pointConstraint( self.objB, self.objA ) )
            constraints.append(\
                orientConstraint( self.objB, self.objA ) )
            constraints.append(\
                scaleConstraint( self.objB, self.objA ) )
        except:
            "Please Select 2 Objects"
            
    def alignThenConstrain(self, isPreparationNeeded=True):   ## This function does not work yet!!!
        if isPreparationNeeded:
            self.prepareForOperation()
        try:
            assert( len(self.objs) == 2 )   
            constraints= []
            constraints.append(\
                pointConstraint( self.objB, self.objA ) )
            constraints.append(\
                orientConstraint( self.objB, self.objA ) )
            constraints.append(\
                scaleConstraint( self.objB, self.objA ) )
            for c in constraints:
                delete( c )
                
            constraints= []
            constraints.append(
                pointConstraint( self.objA, self.objB ) )
            constraints.append(
                orientConstraint( self.objA, self.objB ) )
            constraints.append(
                scaleConstraint( self.objA, self.objB ) )
                
        except:
            "Please Select 2 Objects"
            
            
    
    
    def zero(self, objs=None, originalSelection=None):
        if originalSelection==None:
            originalSelection = ls(selection=True)
        if objs==None:
            objs = originalSelection
        
        zeros = []
        
        for obj in objs:
            ##zero = duplicate( obj )[0]  ## the index is to pull it out of the list
            
            zero = group( empty=True )
            
            select( obj )
            
            parentOfZero = pickWalk(direction = "up")[0] ## we get a list back, so get just the first one
            
            
            
            if parentOfZero==obj:
                print( "obj had no parent")
                
            if parentOfZero==obj:
                parentOfZero=None
            
            self.alignObjAToObjB( zero, obj, originalSelection )
            
            print( obj )
            print( zero )
            print( parentOfZero )
            
            
            
            try:
                parent( obj, w=True )
            except:
                pass
            try:
                parent( zero, w=True )
            except:
                pass
            
            parent( obj, zero )
            
            if parentOfZero:
                parent( zero, parentOfZero )
            
            if obj.name()[-4:] == "Anim":
                zero.rename( obj.name()[0:-4] + "Zero" ) 
            elif obj.name()[-4:] == "__anim":
                zero.rename( obj.name()[0:-4] + "__zero" )
            else:
                zero.rename( obj.name() + "Zero" )
            
            zeros.append( zero )
            
            ## end of for loop
        select( originalSelection )  
        return zero
            
        #try:
            #assert( len(self.objs) == 2 )
        #self.zeros[self.objA] = makeNurbCircle()
        #originalSelection = ls(selection=True)
        
        select( originalSelection)
        
    def pivotFix(self, objs=None, originalSelection=None):
        if originalSelection==None:
            originalSelection = ls(selection=True)
        if objs==None:
            objs = originalSelection
            
        for obj in objs:
            tmpObj = duplicate( obj )
            move ( obj, 0,0,0, rotatePivotRelative=True, scalePivotRelative=True  )
            makeIdentity( obj, apply=True, translate=True, rotate=False, scale=False )
            p = pointConstraint( tmpObj, obj )
            o = orientConstraint( tmpObj, obj )
            s = scaleConstraint( tmpObj, obj )
            delete( p )
            delete( o )
            delete( s )
            delete( tmpObj )
        select( originalSelection )
            
    def replaceObjects(self):
        objs = ls(selection=True)
        objS = objs.pop( )   ## objsO = objs.copy()  Might be useful later

        for objT in objs:
            select(objT)
            shapeToDelete = pickWalk(direction = "down")
            delete(shapeToDelete)

            select(objS)
            tmpObj = duplicate(objS)
            select(tmpObj)
            pickWalk( direction="down" )
            tmpShape = ls(selection=True)
            select( objT, add=True)
            parent( tmpShape, objT, shape=True, relative=True)
            delete( tmpObj )

    

    def makePoleVector(self, constrain=True):
        iks = pm.ls(selection = True )
        originalSelection = iks
        locators = []        
        for ik in iks:
            loc = pm.spaceLocator()
            pm.rename( loc, 'poleVectorTarget' )
            pm.parent( loc, ik )
            ik.poleVectorX >> loc.translateX
            ik.poleVectorY >> loc.translateY
            ik.poleVectorZ >> loc.translateZ
            loc.translateX.disconnect()
            loc.translateY.disconnect()
            loc.translateZ.disconnect()
            pm.parent( loc, world=True )
            if constrain==True:
                pm.poleVectorConstraint( loc, ik, weight=1 )


    def runJointOrientHelper(self):
        try:
            reload( RiggerJointOrientHelper )
        except:
            import RiggerJointOrientHelper
        self.jointOrientHelper = RiggerJointOrientHelper.RiggerJointOrientHelper()
    def runRiveter(self):
        try:
            reload( RiggerRiveter )
        except:
            import RiggerRiveter
        self.riveter = RiggerRiveter.RiggerRiveter()
        
    def runAttributeSetter( self, showUi=True, attribute='', value=''):
        #try:
        #    reload( RiggerAttributeSetter )
        self.attributeSetter = RiggerAttributeSetter(showUi=showUi)
              
    def runAttributeConnector( self, showUi=True ):
        #try:
        #    reload( RiggerAttributeSetter )
        self.attributeConnector = RiggerAttributeConnector(showUi=showUi)
        
    def runRenameByRegex( self, auto_ui=True ):
        self.regexTool = RenameByRegex.RenameByRegex( self, auto_ui=True)
        
    def displayOverrideToWireframe( self ):
        for obj in pm.ls(selection=True):
            obj.overrideEnabled.set( True )
            obj.overrideShading.set( False )
            
    def displayOverrideFromWireframeToNormal( self ):
        for obj in pm.ls(selection=True):
            obj.overrideEnabled.set( False )
            obj.overrideShading.set( True )