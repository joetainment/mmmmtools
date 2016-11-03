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

## Python doc string
"""MmmmToolsUtils - Common Simple Functions For Use In MmmmTools
"""

####################
## Imports
####################
import traceback
import os
import sys
import copy as Copy
import math

import pymel.all as pm
import pymel.tools.mel2py as mel2py    
import maya.OpenMaya as OpenMaya


import pymel.all as pm
import maya.cmds as cmds
import maya.OpenMaya as om
import MmmmToolsMod
import MmmmToolsMod.unipath as unipathimport UtilGetFaceCenter
import UtilsCenterPivotOnSelectedComponents
Pather = MmmmToolsMod.Static.Classes.Pather.PatherUnipath = unipath.Path
class Utils(object):
    logModeDefault = 'file'
    logImportanceDefault = 15
    logMinImportance = 10
    
    centerPivotOnSelectedComponents = \
        UtilsCenterPivotOnSelectedComponents.centerPivotOnSelectedComponents
    
    @classmethod
    def log( cls, *args, **kargs ):
        if kargs.setdefault( 'mode', cls.logModeDefault )=='print':
            im = kargs.setdefault( 'importance', cls.logImportanceDefault )
            if im >= cls.logMinImportance:
                for v in args:
                    print( v )
                trc = traceback.format_exc()
                if trc != 'None\n':  ## The traceback module tacks
                                     ## a newline on format_exc
                    print( "Traceback:")
                    print( trc )
                
    @staticmethod
    def printInfo(msg):
        om.MGlobal.displayInfo(msg)
    @staticmethod
    def printWarning(msg):
        om.MGlobal.displayWarning(msg)
    @staticmethod
    def printError(msg):
        om.MGlobal.displayError(msg)
    
    @staticmethod
    def getMayaPath():
        appEnvFile = pm.about(env=True)
        pathstr, file = os.path.split(appEnvFile)
        upath = Unipath( pathstr ).absolute()
        pather = Pather( upath )
        return pather
        
    @staticmethod    
    def getMainWindowInfo():
        info = Duck()
        mw = pm.getMelGlobal('string', 'gMainWindow')
        ui = pm.PyUI( mw )
        setattr( info, 'mainWindowName', mw )
        setattr( info, 'mainWindow', ui )
        return info
        
    @staticmethod
    def newDuck():
        return Duck()

    @staticmethod
    def camOrthoToggle():
        pm.camera( edit=True, orthographic=True )
        
    @classmethod
    def getActiveCamera(cls):
        cam = cls.getActiveCameraAsString()
        return pm.PyNode(cam)
    
        
    @classmethod
    def getActiveCameraAsString(cls):
        camName = pm.modelPanel(pm.getPanel(wf=True), q=True, cam=True)
        return camName
            
    @classmethod
    def camOrthoToggle(cls):
        cam = cls.getActiveCamera()
        cam.orthographic.set(  not cam.orthographic.get()  )
    
    @staticmethod
    def copyMemberRefsByName( source, target, names ):
        for v in names:
            try:
                target.__dict__[v] = source.__dict__[v]
            except:
                u.log( "Unable To Copy named member ref for name: " + str(v) )


    @staticmethod    
    def getConnectedAttrsFromArrayTypeAttr( arrAttr ):
        connectedAttrs = arrAttr.get() 
        return connectedAttrs

    @staticmethod         
    def getConnectedNodesFromArrayTypeAttr( arrAttr ):
        conneectedAttrs = Utils.getConnectedAttrsFromArrayTypeAttr( arrAttr )
        connectedNodes = [ pm.PyNode( a.split('.')[0] ) for a in conneectedAttrs ]
        return connectedNodes
        
    @staticmethod
    def printInfo(roundNumbersForCenters=True, precision=1):
            return UtilGetFaceCenter.getFaceCenter(
                roundNumbersForCenters=roundNumbersForCenters,
                precision=precision
            )

    
    @staticmethod    
    def importCode( name, code, add_to_sys_modules=0, vars_dict=None):
        print("This is running in the importCode function.")
        import sys,imp
    
        module = imp.new_module(name)
    
        if not vars_dict is None:
            try:
                if vars_dict.get('self',None)=='specialMmmmToolsMagicToken_this_var_will_be_replaced':
                    vars_dict['self']=module
                for k in vars_dict.keys():
                    try:
                        module.__dict__[k] = vars_dict[k]
                    except:
                        print ( traceback.format_exc()  )
                        print ( "Could not add default convenience vars to new module, but continuing anyway." )
            except:
                print ( traceback.format_exc()  )
                print ( "Could not add default conveience vars to new module, but continuing anyway." )
    
        exec code in module.__dict__
        if add_to_sys_modules:
            sys.modules[name] = module
    
        return module
        
    @staticmethod    
    def toggleWireframeOnShaded( ):
        pm.mel.eval(
        """
        {string $curPanel; $curPanel = `getPanel -withFocus`; int $x=`modelEditor -q -wos $curPanel`; $x = ($x*-1)+1; setWireframeOnShadedOption $x $curPanel;}
        """
        )           
    
    ## Crease Edges Functions #### DeprecationWarning - use version in Static.Mesh
    #### DeprecationWarning - use version in Static.Mesh
    @classmethod
    def creaseSelectedEdges(cls):
        cls.setCreaseValueOnSelection( 20.0 )
    #### DeprecationWarning - use version in Static.Mesh        
    @classmethod
    def uncreaseSelectedEdges(cls):
        cls.setCreaseValueOnSelection( 0.0 )
    
    #### DeprecationWarning - use version in Static.Mesh
    @staticmethod
    def setCreaseValueOnSelection( v ):
        objs = pm.ls(selection=True) ## removed flatten=True because it makes it crazy slow
        for obj in objs:
            try:
                creaseValue = pm.polyCrease( obj, value = v )
            except:
                pass  ## we don't care if this fails, no big deal

        @staticmethod    def hyperGraphAsActivePanelShowShapesToggle():

        hpPanelName = pm.mel.eval( 'getPanel("-withFocus");' )
        edName = hpPanelName + "HyperGraphEd"


        oldValue = pm.hyperGraph( edName, query=True, showShapes=True )

        newShowShapesValue = 0

        if oldValue == 0:
            newShowShapesValue = 1
            

        pm.hyperGraph( edName, edit=True, showShapes=newShowShapesValue )
    #### DeprecationWarning - use version in Static.Mesh        
    @staticmethod
    def convertSelectionToCreasedEdges():
        pm.mel.eval( "ConvertSelectionToEdges;" )
        objs = pm.ls(selection=True, flatten=True)
        objsToSelect = []
        for obj in objs:
            try:
                creaseValue = pm.polyCrease( obj, query=True, value=True )
                creaseValue = creaseValue[0]
            except:
                creaseValue = 0

            if creaseValue > 0.01:
                #print( "found a creased edge" )
                objsToSelect.append(obj)

        if len(objsToSelect) > 0:
            #print(objsToSelect)
            #print("selecting")    
            pm.select( objsToSelect, replace=True )
        else:
            pm.select( clear=True )
    
    #### DeprecationWarning - use version in Static.Mesh        
    @staticmethod
    def convertSelectionToHardEdges():
        pm.mel.eval( "ConvertSelectionToEdges;" )
        cmps = pm.ls(selection=True, flatten=True )
        to_select = []
        for cmp in cmps:
            if cmp.isSmooth()==False:
                to_select.append( cmp )
        pm.select( to_select )
    
    #### DeprecationWarning - use version in Static        
    @staticmethod
    def setAttributeOnSelected( attrName, v ):
        objs = pm.ls(selection=True, flatten=True)
        for obj in objs:
            try:
                obj.setAttr( attrName, v )
            except:
                print("Could not affect " + obj )
    
    
    
    
    
    @staticmethod
    def saveIncrementally():

        fullPathFilename = pm.sceneName()

        parts = fullPathFilename.split('/')
        directory = parts[ 0 : -1 ]
        directory = '/'.join( directory )
        print directory

        filename_w_ext = parts[-1]
        print filename_w_ext

        filename_split_by_dot = filename_w_ext.split('.')
        
        filename_no_ext = '.'.join( filename_split_by_dot[:-1] )
        ext = filename_split_by_dot[-1]
        print filename_no_ext
        print ext

        reversal = list( filename_no_ext )
        reversal.reverse()
        reversal = ''.join( reversal )
        print reversal

        digits_at_end = 0
        digits_as_symbols = ['0','1','2','3','4','5','6','7','8','9']

        for symbol in reversal:
          if symbol in digits_as_symbols:
            digits_at_end = digits_at_end + 1
          else:
            break

        if digits_at_end > 0:
            filename_no_digits = filename_no_ext[0 : -digits_at_end ]
            filename_digits = filename_no_ext[-digits_at_end:]
            file_version_number = int(filename_digits)
            print filename_no_digits
            print filename_digits
        else:
            filename_no_digits = filename_no_ext
            file_version_number = 0
        
        
        incremented_number = file_version_number + 1

        incremented_number = str(incremented_number)
        incremented_number = incremented_number.zfill( digits_at_end )
        
        filename_incremented = filename_no_digits + incremented_number
        
        filename_incremented_w_ext = filename_incremented + '.' + ext

        filename_w_fullpath = directory + '/' + filename_incremented_w_ext

        import maya.cmds as cmds
        
        cmds.file( rename = filename_w_fullpath )
        if ext=='mb':
            cmds.file( save=True, type='mayaBinary' )
        else:
            cmds.file( save=True, type='mayaAscii' )

    @classmethod
    def moveUpInHierarchy( cls ):

        origSel = pm.ls(selection=True)
        
        for obj in origSel:
            par = None
            gpar = None
            
            par = obj.getParent()
            
            if par is not None:    
                gpar = par.getParent()
            
                if gpar is None:
                    pm.parent( obj, world=True )
                
                else:
                    pm.parent( obj, gpar )  

    @staticmethod
    def selectionConversionFromFaceToEdgeBorder():
            pm.mel.eval( """select -r `polyListComponentConversion -ff -te -bo`;""" )
            
    

    @classmethod
    def convertMelToPython(cls, melStr=""):
        #import pymel.tools.mel2py as mel2py    is at top of file
        pyStr = mel2py.mel2pyStr( melStr )
        return pyStr
    
    @classmethod
    def doTransfer( cls, spa="",
                    uvs=1, colors=0, positions=0, normals=0,
                    srcUvSet=None, targetUvSet=None  ):

        osel = pm.ls(selection=True)
        
        objs = osel[:]
        
        src = objs.pop(0)

        if type(spa)==type(1):
            spa = spa
        else:
            spa = 5

        for obj in objs:
            
            try:
                o = obj.getShape()
            except:
                o = obj
            try:
                s = src.getShape()
            except:
                s = src
                
            
            try:    
                if srcUvSet == None:
                    suvs = pm.polyUVSet( s, query=True, currentUVSet=True )
                else:
                    suvs = srcUvSet
                if targetUvSet == None:                
                    tuvs = pm.polyUVSet( o, query=True, currentUVSet=True )
                else:
                    tuvs = targetUvSet
                
                pm.transferAttributes( s, o,
                    transferUVs=uvs,
                    transferColors=colors,
                    transferPositions=positions,
                    transferNormals=normals,
                    sourceUvSpace=str(suvs),
                    targetUvSpace=str(tuvs),
                    spa=spa
                )
                ## spa is  	Selects which space the attribute transfer
                ##is performed in. 0 is world space, 1 is model space,
                ## 4 is component-based, 5 is topology-based.
                ## The default is world space.
            except:
                print( "Could not complete one of the transfer operations." )
                print(  traceback.format_exc()  )
                    
                
            
            
    

class UiUtils(object):
    @staticmethod
    def getMayaWindowAsWrappedInstance(  ):
        try:
            from PySide import QtGui as ModQtGui
            from PySide import QtCore as ModQtCore
            import shiboken as ModShiboken
            import maya.OpenMayaUI as ModOpenMayaUI
            windowPtr = ModOpenMayaUI.MQtUtil.mainWindow()
            if not  windowPtr is None:
                return ModShiboken.wrapInstance(
                    long(windowPtr), ModQtGui.QMainWindow
                )
        except:
            print( "This app is probably not running inside Maya" )
            print( traceback.format_exc()  )
                
    
    @classmethod
    def createUiQDialogInMaya( cls ):
        mwin = cls.getMayaWindowAsWrappedInstance()
        import PySide.QtGui as ModQtGui
        return ModQtGui.QDialog( mwin )
    
    
    @classmethod
    def infoPrompt(cls, msg='message', title='Maya' ):
        cls.prompt( msg=msg, title=title, okOnly=True )
        return None

    @staticmethod
    def prompt( msg='', opts=None, typeToReturn=None, okOnly=False, returnEmptyStringAsNone=True, **kargs ):
        """
        Get a prompt and as soon as it's done, return the results.
        Can be told to return a string, int or float using:
        typeToReturn='string' or 'int' or 'float'
        
        
        By default if the user enters nothing,
        the return value will be: None
        
        Most of the time this is useful so the return value doesn't have to be checked to ensure
        it isn't an empty string.
        
        To return empty strings instead, set 
        returnEmptyStringAsNone to False
        """
        if opts is None:
            opts = kargs
    
        opts.setdefault( 'message', msg )
        opts.setdefault( 'title', 'Maya' )
        if okOnly:
            opts.setdefault( 'button', [ 'OK' ] )
        else:
            opts.setdefault( 'button', [ 'OK', 'Cancel'] )   
        opts.setdefault( 'dismissString', 'Cancel' )        

        
        if okOnly:
            result = pm.confirmDialog(**opts)
            text = None
        else:
            result = pm.promptDialog(**opts)
            if result == 'OK':
                text = pm.promptDialog(query=True, text=True)
            else:
                text =  None
        
        if returnEmptyStringAsNone:
            ## at this point text should always be in string-like form
            ## or the None object
            ## it won't be an int or float or something yet
            ## so it's safe to test it this way
            if not text:  
                text = None
        
        if not text is None:
            if typeToReturn == 'string':
                text = str(text)
            if typeToReturn == 'float':
                text = float(text)
            elif typeToReturn=='int':
                text = int(text)
            return text
        else:
            return text
        
    @classmethod
    def setProjectByStringUi(cls):     
        dialogResult = pm.promptDialog(
                title='Set Project',
                message='Type or Paste Project Path Here:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')

        if dialogResult == 'OK':
            response = pm.promptDialog(query=True, text=True).replace( "\\", "/" )
            ## The maya mel proceedure set project would have to be reverse engineered
            ## and rewritten in Python in order to work.
            ## Instead, we just use mel.  Some funny characters
            ## Might cause problems, but that would be a rare case
            ## and in those cases, the default maya setProject tool
            ## could be used.
            pm.mel.eval( "setProject " + '"' + response + '"' + ";" )            
        
    
        

class Duck(object):
    """
    A mostly empty class that is just used for organization.
    To store various variable in it's __dict__
    Allow us to do things like:  myDuck.x = 1; myDuck.y="y wasn't a member before now"
    We can't use object directly, since they don't allow new members using this syntax
    so we need to make something that inherits from it.
    """
    pass        
        
    

