"""
Viewer - Module containing functionality relating to 
    viewing objects, viewport controls, camerea, etc
"""

import pymel.all as pm
import pymel
import maya.cmds as cmds
import maya
import maya.OpenMaya as om

import traceback, math, random

import collections


#try
#    reload(SelectorVolumeSelect)
#except
#    try
#        import SelectorVolumeSelect
#    except
#        print( traceback.format_exc() )



class Commander(object):
    def __init__(self, parentRef):
        self.parent = parentRef
        self.mmmm = self.parent
        self.commands = collections.OrderedDict()
        self.uiMenuItems = collections.OrderedDict()
        self.commandsMelNames = collections.OrderedDict()
        self.addCommand( 'Commander/Hello', self.hello )
        self.addCommand( 'Commander/List', self.listCommands )

    def listCommands(self):
            for k in self.commands.keys():
                print( k )
        
    def listCommandsMelNames(self, showKeys = False):
        if showKeys==False:
            for v in self.commandsMelNames.values():
                print( v )
        else:
            for k, v in self.commandsMelNames.items():
                print( k )
                print( v )
    
    def getMmmmCmd( self, name ):
        return self.commandsMelNames.get(name,None)
    
    def addCommand(self, name, func, annotation=None, uiMenuItem=None ):
    
        cmdName = 'MmmmCmds__' + name.replace('/','__')
    
        self.commands[name]=func
        self.commandsMelNames[name] = cmdName
    
        if annotation==None:
            cmdAnnotation = cmdName + 'Annotation'
        else:
            cmdAnnotation = cmdName + '_' + annotation
            

    
        try:
            if cmds.runTimeCommand( cmdName, q=True, exists=True ):
                cmds.runTimeCommand( cmdName, e=True, delete=True )
                
            cmds.runTimeCommand(
                cmdName,
                annotation=cmdAnnotation,
                category="Custom Scripts",
                commandLanguage="python",
                hotkeyCtx="",
                command="mmmmTools.commander.commands['" + name + "']()"
            )
        except:
            print( "Error Creating Runtime Command" )                            
            print( traceback.format_exc()  )        

        #if uiMenuItem!=None:
            
            
    
        
    def hello(self):
        om.MGlobal.displayInfo( "Hello From Commander!")
        